# vim: fileencoding=utf8
from cStringIO import StringIO
from xml.dom.minidom import parseString
import logging
import codecs
import datetime
import time
import struct
import urllib2
import amf, amf0, amf.utils

RESPONSE_RESULT = '/onResult'
RESPONSE_STATUS = '/onStatus'
# RESPONSE_DEBUG_EVENTS = '/onDebugEvents'


class AMFMessageBody(object):

    def __init__(self, target, response, data):
        self.target = target
        self.response = response
        self.data = data
        self.__service_name = None
        self.__service_method_name = None

    def __get_service_method_path(self):
        if not self.__service_name or not self.__service_method_name:
            self.__setup_target()
        return self.__service_name + '/' + self.__service_method_name
    service_method_path = property(__get_service_method_path)

    def __setup_target(self):
        dotIndex = self.target.rfind('.')
        if dotIndex > 0:
            self.__service_name = self.target[:dotIndex]
            self.__service_method_name = self.target[dotIndex+1:]

    def __get_args(self):
        if isinstance(self.data, (tuple, list)):
            return self.data
        return []
    args = property(__get_args)

    def _get_cache_key(self):
        self.target + str(self.data)
         
    def __str__(self):
        return "target=%s,response=%s,data=%s" % (self.target, self.response, self.data)


class AMFMessage(object):

    def __init__(self):
        self.headers = []
        self.headerMap = {}
        self.bodies = []
        self.version = 3
        self.use_cache = False

    def add_header(self, amfHeader):
        """
        Add AMF header to this message.
        
        amfHeader parameter is a dict object which contains 'name' and 'content' key.
        It may contain 'mustUnderstand' key.
        """
        self.headers.append(amfHeader)
        self.headerMap[amfHeader['name']] = amfHeader['content']
        if amfHeader['name'].lower() == 'use-cache':
            self._set_cache(amfHeader)

    def get_header(self, name):
        return self.headerMap.get(name, None)

    def _set_cache(self, amfHeader):
        if int(amfHeader['content']) > 0:
            self.use_cache = True
            self.cache_timeout = int(amfHeader['content'])
        else:
            self.use_cache = False
            self.cache_timeout = 0

    def add_body(self, amfBody):
        self.bodies.append(amfBody)

    def get_body_count(self):
        return len(self.bodies)

    def __str__(self):
        return "AMFMessage object [%d headers, %d bodies]" % (len(self.headers), len(self.bodies))


class AMFMessageBodyContext(object):

    def __init__(self):
        self._str_refs = []
        self._obj_refs = []
        self._class_def_refs = []

    def add_string_reference(self, str):
        amf.utils.logger().debug("add_string_reference(%s) -- index='%d'", repr(str), len(self._str_refs))
        self._str_refs.append(str)

    def get_string_reference(self, index):
        str = self._str_refs[index]
        amf.utils.logger().debug("get_string_reference(%d) -- %s", index, repr(str))
        return str

    def get_string_reference_index(self, str):
        try:
            return self._str_refs.index(str)
        except ValueError:
            return -1

    def add_object_reference(self, obj):
        amf.utils.logger().debug("add_object_reference(%s) -- index='%d'", repr(obj), len(self._obj_refs))
        self._obj_refs.append(obj)

    def get_object_reference(self, index):
        obj = self._obj_refs[index]
        amf.utils.logger().debug("get_object_reference(%d) -- %s", index, repr(obj))
        return obj

    def get_object_reference_index(self, obj):
        try:
            return self._obj_refs.index(obj)
        except ValueError:
            return -1

    def add_class_def_reference(self, class_def):
        amf.utils.logger().debug("add_class_def_reference(%s) -- index='%d'", repr(class_def), len(self._class_def_refs))
        self._class_def_refs.append(class_def)

    def get_class_def_reference(self, index):
        class_def = self._class_def_refs[index]
        amf.utils.logger().debug("get_class_def_reference(%d) -- %s", index, repr(class_def))
        return class_def

    def get_class_def_reference_index(self, class_def):
        try:
            return self._class_def_refs.index(class_def)
        except ValueError:
            return -1


class ByteArray(object):

    def __init__(self, data):
        self.data = data


class AMFAuthenticationError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def read(raw_post_data, options={}):
    """
    Parse the given data and return the AMFMessage object.
    """
    # for debug
    #__write_data_to_file(raw_post_data)
    return amf0.read(raw_post_data, options)

def __write_data_to_file(data):
    """
    Write the given data to '/tmp/postdata.dat'.
    This function is for debugging.
    """
    import os, os.path
    dir = os.environ['TMP']
    file = os.path.join(dir, 'postdata.dat')
    f = open(file, 'wb')
    f.write(data)
    f.close()

def write(message):
    """
    Convert the given AMFMessage object to binary data, and return it.
    """
    amf_version = message.version
    if amf_version == 3:
        import amf3
        return amf3.write(message)
    else:
        return amf0.write(message)

