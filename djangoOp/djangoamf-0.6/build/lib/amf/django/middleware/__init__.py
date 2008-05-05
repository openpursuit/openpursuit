# vim: fileencoding=utf8
import logging
import re
import types
import amf, amf.utils, amf.django
from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden
from django.db.models.query import QuerySet
from django.core import exceptions, urlresolvers

class AMFMiddleware(object):

    CONTENT_TYPE = 'application/x-amf'
    AUTO_MAPPING_VIEW_NAME = 'amf.django.views'

    def __init__(self):
        """Initialize AMFMiddleware."""
        self.init_logger()
        self.init_class_mapper()
        self.init_timezone()
        self.init_read_options()

        self.gateway_path = getattr(settings, 'AMF_GATEWAY_PATH', '/gateway/')
        if not self.gateway_path:
            msg = "'AMF_GATEWAY_PATH' is not set in 'settings.py'"
            amt.utils.logger().fatal(msg)
            raise AttributeError, msg
        self.matcher = re.compile(r"^%s.+" % (self.gateway_path))
        amf.utils.logger().debug("AMFMiddleware was initialized.") 

    def init_timezone(self):
        amf.utils.timeoffset = getattr(settings, 'AMF_TIME_OFFSET', None)

    def init_class_mapper(self):
        mapper_name = getattr(settings, 'AMF_CLASS_MAPPER', None)
        if mapper_name:
            amf.utils.logger().debug("Init AMF class mappings.")
            try:
                mapper = amf.utils.get_module(mapper_name)
            except ImportError:
                msg = "AMF_CLASS_MAPPER module is not found. [module='%s']" % (mapper_name,)
                amf.utils.logger().fatal(msg)
                raise ImportError(msg)

            if mapper and getattr(mapper, 'amf_class_mappings', False):
                mappings = mapper.amf_class_mappings()
                if isinstance(mappings, dict):
                    amf.utils.class_mappings = mappings
                else:
                    msg = "The return value of amf_class_mappings() is not a dictionary type. [type='%s']" % (type(mappings),)
                    amf.utils.logger().fatal(msg)
                    raise TypeError(msg)
            else:
                msg = "'amf_class_mappings' function is not defined in AMF_CLASS_MAPPER module. [module='%s']" % (mapper_name,)
                amf.utils.logger().fatal(msg)
                raise AttributeError(msg)

    def init_logger(self):
        """Build custom logger instance for AMF handling."""
        # TODO: Logging time is not a local time
        file = getattr(settings, 'AMF_LOG_FILE', None)
        mode = getattr(settings, 'AMF_LOG_FILE_MODE', 'a')
        encoding = getattr(settings, 'AMF_LOG_FILE_ENCODING', 'utf8')
        loglevel = getattr(settings, 'AMF_LOG_LEVEL', 'INFO')

        logger = logging.getLogger('AMF')
        logger.setLevel(logging.__dict__[str(loglevel).upper()])
        if file:
            handler = logging.FileHandler(filename=file, mode=mode, encoding=encoding)
            formatter = logging.Formatter('%(asctime)s - %(name)s %(filename)s(%(lineno)d) [%(levelname)s] %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        amf.utils.set_logger(logger)

    def init_read_options(self):
        self.read_options = {}
        if getattr(settings, 'AMF_NUMBER_TO_INT', False):
            self.read_options['number_to_int'] = True

    def process_request(self, request):
        if self.matcher.match(request.path): # Invalid access
            return HttpResponseForbidden()
        elif request.method == 'POST' and \
                request.path == self.gateway_path and \
                (request.META.get('HTTP_CONTENT_TYPE') == AMFMiddleware.CONTENT_TYPE or request.META.get('CONTENT_TYPE') == AMFMiddleware.CONTENT_TYPE):
            # Deserialize AMF message
            request_message = amf.read(request.raw_post_data, self.read_options)

            #if request_message.use_cache: # Get cached data
            #    key = request_message._get_cache_key()
            #    if key:
            #        from django.core.cache import cache
            #        cached_response = cache.get(key)
            #        if cached_response: # If cached data found, return it
            #            return cached_response

            self.set_credentials(request_message, request)

            # Build AMF response message
            response_message = amf.AMFMessage()
            response_message.version = request_message.version
            for request_body in request_message.bodies:
                res_body = self.process_request_message_body(request, request_body)
                response_message.add_body(res_body)
            self._add_response_headers(response_message)
            # Serialize AMF message
            response_data = amf.write(response_message)
            response = HttpResponse(response_data, AMFMiddleware.CONTENT_TYPE)
            response['Content-Length'] = str(len(response_data))

            #if request_message.use_cache: # Cache response data
            #    key = request_message._get_cache_key()
            #    if key:
            #        from django.core.cache import cache
            #        cache.set(key, response, request_message.cache_timeout)

            return response

    def process_request_message_body(self, request, request_body):
        path = request.path + request_body.service_method_path
        resolver = urlresolvers.RegexURLResolver(r'^/', settings.ROOT_URLCONF)
        try:
            callback, callback_args, callback_kwargs = resolver.resolve(path)
            # Find callback method for auto method mapping.
            if callback.__module__ + '.' + callback.__name__ == self.AUTO_MAPPING_VIEW_NAME:
                callback = self.find_callback_method(callback_args, callback_kwargs)
        except Exception, e:
            result = {
                    'description': "Cannot find a view for the path ['%s'], %s" % (path, e),
                    'details'    : "Cannot find a view for the path ['%s'], %s" % (path, e),
                    'type'       : 'AMFRuntimeException',
                    'code'       : 0
                    }
            res_target = request_body.response + amf.RESPONSE_STATUS
        else:
            try:
                #
                # *** Invoking the view function here ***
                #
                result = callback(request, *request_body.args)
                # Convert django's QuerySet object into an array of it's containing objects.
                if isinstance(result, QuerySet): result = list(result)
                res_target = request_body.response + amf.RESPONSE_RESULT
            except amf.AMFAuthenticationError, e:
                msg = "Exception was thrown when executing remoting method.(%s) [method=%s, args=%s]" % (e, callback.__module__ + "." + callback.__name__, repr(request_body.args))
                result = {
                        'description' : str(e),
                        'details'     : msg,
                        'type'        : e.__class__.__name__,
                        'code'        : 401
                        }
                res_target = request_body.response + amf.RESPONSE_STATUS
            except Exception, e:
                msg = "Exception was thrown when executing remoting method.(%s) [method=%s, args=%s]" % (e, callback.__module__ + "." + callback.__name__, repr(request_body.args))
                # TODO: This can bring about UnicodeDecodeError in logging module
                #amf.utils.logger().error(msg)

                result = {
                        'description' : str(e),
                        'details'     : msg,
                        'type'        : 'AMFRuntimeException',
                        'code'        : 500
                        }
                res_target = request_body.response + amf.RESPONSE_STATUS
                self._send_error_mail(request)
        return amf.AMFMessageBody(res_target, 'null', result)

    def _send_error_mail(self, request):
        """Send error mail to admins."""
        if not settings.DEBUG:
            from django.core.mail import mail_admins
            import sys
            exc_info = sys.exc_info()
            subject = 'Error (%s IP): %s' % ((request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS and 'internal' or 'EXTERNAL'), "AMF gateway " + request.path)
            try:
                request_repr = repr(request)
            except:
                request_repr = "Request repr() unavailable"
            message = "%s\n\n%s" % (self._get_traceback(exc_info), request_repr)
            mail_admins(subject, message, fail_silently=True)

    def _get_traceback(self, exc_info=None):
        """Helper function to return the traceback as a string"""
        import traceback
        return '\n'.join(traceback.format_exception(*(exc_info or sys.exc_info())))

    def find_callback_method(self, callback_args, callback_kwargs):
        mod = callback_kwargs['views']
        if isinstance(mod, types.StringTypes):
            mod_name = mod
            mod = amf.utils.get_module(mod_name)
        elif isinstance(mod, types.ModuleType):
            mod_name = mod.__name__
        else:
            amf.utils.logger().error("The type of 'views' value for amf.django.views is invalid.")
            raise TypeError
        method_name = callback_args[0]
        amf.utils.logger().debug("Using auto method mapping. [module='%s', method='%s']", mod_name, method_name)
        callback = getattr(mod, method_name)
        return callback

    def set_credentials(self, request_message, request):
        """
        If the request amf message has headers for credentials, set them to
        the given request object.

        The request object has an attribute named 'amfcredentials' which is a
        dict holding two keys, 'username' and 'password'.

        request.amfcredentials.get('username')
        request.amfcredentials.get('password')
        """
        username = request_message.get_header("credentialsUsername")
        password = request_message.get_header("credentialsPassword")
        if username is not None and password is not None:
            request.amfcredentials = {'username':username, 'password':password}

    def _add_response_headers(self, message):
        for h in amf.django.get_response_headers():
            message.add_header(h)

