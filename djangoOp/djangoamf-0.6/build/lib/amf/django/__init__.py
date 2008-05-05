# vim: fileencoding=utf8
import os.path
import re
from types import *
import amf, amf.utils
from django.conf import settings

def views():
    pass

def save_to_file(data, filename, dir=None):
    """
    Saves the given data to a file, and returns the dict object
    holding path and url keys.

    To use this function, MEDIA_ROOT and MEDIA_URL must be
    set in Django configuration file.
    """
    if isinstance(data, amf.ByteArray):
        data = data.data
    if dir:
        filename = os.path.join(dir, filename)
    path = os.path.join(settings.MEDIA_ROOT, filename)
    file = open(path, 'wb')
    try:
        file.write(data)
    except:
        raise
    else:
        file.close()
    url = os.path.join(settings.MEDIA_URL, filename)
    url = re.sub(r'\\', '/', url)
    return { 'path':path, 'url':url }

def delete_file(filename, dir=None):
    """
    Delete the file located in MEDIA_ROOT directory.
    If the operation fails or the target file doesn't exist, return False.
    """
    if dir:
        filename = os.path.join(dir, filename)
    path = os.path.join(settings.MEDIA_ROOT, filename)
    if os.path.exists(path):
        try:
            os.remove(path)
            return True
        except:
            pass
    return False

def __get_user_permissions(request):
    """
    Returns the all permissions which the authenticated user has.
    The type of the return value is string, list, or tuple.
    If the user has no permission, an empty tuple is returned.
    """
    auth_func = getattr(settings, 'AMF_AUTH_FUNC')
    if hasattr(request, 'amfcredentials'):
        username = request.amfcredentials.get('username', None)
        password = request.amfcredentials.get('password', None)
    else:
        username = None
        password = None
    if isinstance(auth_func, FunctionType):
        result = auth_func(request, username, password)
    elif isinstance(auth_func, StringTypes):
        func = amf.utils.get_func(auth_func)
        result = func(request, username, password)

    if isinstance(result, (StringTypes, ListType, TupleType)):
        return result
    else:
        return ()

def __authenticate(perm, request):
    """
    Checks if the user has a valid permssion for processing the requested method.

    perm -- Required permission. Multiple permissions can be specified. They have to be delimited with comma or space.
    request -- Request object.
    """
    p = re.compile(r'[\s,]+')
    permissions = p.split(perm)
    user_permissions = __get_user_permissions(request)
    for p in permissions:
        if p in user_permissions:
            return True
    return False

def permission_required(perm):
    def func_wrapper(func):
        def wrapper(request, *args):
            if __authenticate(perm, request):
                return func(request, *args)
            else:
                raise amf.AMFAuthenticationError("The user does not have access to '%s'" % (func.__name__,))
        return wrapper
    return func_wrapper

def __assert_using_django_auth_system():
    auth_func = getattr(settings, 'AMF_AUTH_FUNC', None)
    if auth_func is not None:
        if (isinstance(auth_func, StringTypes) and auth_func == 'amf.django.authenticate') or (isinstance(auth_func, FunctionType) and auth_func.__name__ == 'amf.django.authenticate'):
            return True
    raise NotImplementedError, 'Django AMF does not use Django\'s authentication system.'

def login_required(func):
    def wrapper(request, *args):
        __assert_using_django_auth_system()
        import django.contrib.auth as dca
        if request.user.is_authenticated():
            return func(request, *args)
        else:
            if hasattr(request, 'amfcredentials'):
                username = request.amfcredentials.get('username', None)
                password = request.amfcredentials.get('password', None)
                user = dca.authenticate(username=username, password=password)
                if user is not None and user.is_active:
                    dca.login(request, user)
                    return func(request, *args)
        raise amf.AMFAuthenticationError("The user does not have access to '%s'" % (func.__name__,))
    return wrapper

def logout(func):
    def wrapper(request, *args):
        __assert_using_django_auth_system()
        import django.contrib.auth as dca
        dca.logout(request)
        return func(request, *args)
    return wrapper

def authenticate(request, username, password):
    import django.contrib.auth as dca
    if request.user.is_authenticated():
        loggedin = True
        user = request.user
    else:
        loggedin = False
        user = dca.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        if not loggedin:
            dca.login(request, user)
        if user.is_superuser:
            perms = dca.models.Permission.objects.all()
            return [ p.codename for p in perms]
        return user.get_all_permissions()
    return ()

def add_response_header(name, value, mustUnderstand=False):
    """
    Add an AMF header included in a response AMF message.
    """
    thread_local = amf.utils.get_thread_local()
    headers = getattr(thread_local, 'amfHeaders', [])
    headers.append({
        'name'           : name,
        'value'          : value,
        'mustUnderstand' : mustUnderstand
        })
    setattr(thread_local, 'amfHeaders', headers)

def get_response_headers():
    thread_local = amf.utils.get_thread_local()
    return getattr(thread_local, 'amfHeaders', [])

