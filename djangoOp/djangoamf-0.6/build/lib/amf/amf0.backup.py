# vim: fileencoding=utf8
import codecs
import struct
import re
import datetime
import time
import socket
from decimal import Decimal
from types import *
try:
    set
except NameError:
    from sets import Set as set, ImmutableSet as frozenset
import xml.dom.minidom as minidom
import amf, amf.utils
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


DOUBLE         = 0x00
BOOL           = 0x01
UTF8           = 0x02
OBJECT         = 0x03
MOVIECLIP      = 0x04
NULL           = 0x05
UNDEFINED      = 0x06
REFERENCE      = 0x07
MIXED_ARRAY    = 0x08
END_OF_OBJECT  = 0x09
ARRAY          = 0x0A
DATE           = 0x0B
LONG_UTF8      = 0x0C
UNSUPPORTED    = 0x0D
RECOREDSET     = 0x0E
XML            = 0x0F
TYPED_OBJECT   = 0x10
AMF3_DATA_TYPE = 0x11


read_func_map = {
    DOUBLE         : 'read_double',
    BOOL           : 'read_boolean',
    UTF8           : 'read_utf',
    OBJECT         : 'read_object',
    MOVIECLIP      : None,
    NULL           : None,
    UNDEFINED      : None,
    REFERENCE      : 'read_reference',
    MIXED_ARRAY    : 'read_mixed_array',
    ARRAY          : 'read_array',
    DATE           : 'read_date',
    LONG_UTF8      : 'read_long_utf',
    UNSUPPORTED    : None,
    XML            : 'read_xml',
    TYPED_OBJECT   : 'read_custom_class',
    AMF3_DATA_TYPE : 'read_amf3_data',
}

__number_to_int = False

def read_byte(input, context=None):
    return ord(input.read(1))

def read_int(input, context=None):
    return ((ord(input.read(1)) << 8) | ord(input.read(1)));

def is_int(value):
    return int(value) == value

def read_double(input, context=None):
    bytes = input.read(8)
    float_value = struct.unpack('!d', bytes)[0]
    if __number_to_int and is_int(float_value):
        return int(float_value)
    return float_value

def read_boolean(input, context=None):
    return read_byte(input) == 1

def read_utf(input, context=None, length=None):
    if length is None:
        length = read_int(input)
    if length == 0:
        return ''
    return input.read(length)

def read_data(input, type, context):
    if type not in read_func_map:
        amf.logger.error("Unsupported Type [type='%s']", type)
        raise Exception("Unsupported type [type='%s']" % (type,))
    func_name = read_func_map[type]
    if func_name is not None:
        func = eval(func_name)
        if callable(func):
            return func(input, context)
    return None

def read_object(input, context):
    key = read_utf(input, context)
    type = read_byte(input, context)
    ret = {}
    while type != END_OF_OBJECT:
        val = read_data(input, type, context)
        ret[key] = val
        key = read_utf(input, context)
        type = read_byte(input)
    return ret
    
def read_reference(input, context):
    reference = read_int(input, context);
    return "(unresolved object #%s)" % reference

def read_mixed_array(input, context):
    input.read(4)
    return read_mixed_object(input, context)

def read_mixed_object(input, context):
    key = read_utf(input, context)
    type = read_byte(input)
    ret = {}
    while type != END_OF_OBJECT:
        val = read_data(input, type, context)
        if isinstance(key, (int, long, float)):
            key = float(key)
        ret[key] = val
        key = read_utf(input, context)
        type = read_byte(input)
    return ret
    
def read_long(input, context=None):
    return ((ord(input.read(1)) << 24) |
            (ord(input.read(1)) << 16) |
            (ord(input.read(1)) << 8) |
            ord(input.read(1)))

def read_array(input, context):
    ret = []
    length = read_long(input)
    for i in range(length):
        type = read_byte(input)
        ret.append(read_data(input, type, context))
    return ret

def read_date(input, context):
    ms = read_double(input) # date in milliseconds from 01/01/1970
    offset = read_int(input)
    if offset > 720:
        offset = - (65536 - offset)
    offset *= -60
    h = offset / 3600
    class TZ(datetime.tzinfo):
        def utcoffset(self, dt):
            return datetime.timedelta(hours=h)
        def dst(self, dt):
            return datetime.timedelta(0)
        def tzname(self, dt):
            return "JST" # TODO: How to deal with other timezone?
    tz = TZ()  
    return datetime.datetime.fromtimestamp(ms / 1000.0, tz) 

def read_long_utf(input, context=None):
    length = read_long(input)
    val = input.read(length)
    return val

def read_xml(input, context=None):
    xmlStr = read_long_utf(input)
    return minidom.parseString(xmlStr)

def read_custom_class(input, context):
    type = read_utf(input).replace('..', '')
    obj = read_object(input, context)
    amf.utils.logger().debug("read_custom_class() -- type=%s, object=%s", type, str(obj))
    if '_explicitType' not in obj:
        obj['_explicitType'] = type
    return amf.utils.classcast(type, obj)

def read_amf3_data(input, context):
    import amf3
    return amf3.read_data(input, context)

def read_headers(input, message):
    read_byte(input)
    version = read_byte(input) # client -- 0x00: FP 8 or below, 0x01: FMS, 0x03: FP 9
    message.version = version
    header_count = read_int(input)
    for i in range(header_count):
        context = None
        if (message.version == 3):
            context = amf.AMFMessageBodyContext()
        name = read_utf(input)
        mustUnderstand = read_boolean(input)
        input.seek(4, 1) # Length in bytes of header
        type = read_byte(input)
        content = read_data(input, type, context)
        amfHeader = { 'name':name, 'mustUnderstand':mustUnderstand, 'content':content }
        message.add_header(amfHeader)

def read_bodies(input, message):
    bodyCount = read_int(input)
    for i in range(bodyCount):
        context = None
        if (message.version == 3):
            context = amf.AMFMessageBodyContext()
        target = read_utf(input)
        response = read_utf(input)
        input.read(4) # Body length in bytes
        type = read_byte(input)
        amf.utils.logger().debug("AMF Type='%s'", type)
        value = read_data(input, type, context)
        amf_body = amf.AMFMessageBody(target, response, value)
        message.add_body(amf_body)

def read(raw_post_data, options={}):
    __number_to_int = options.get('number_to_int', False)

    input = StringIO(raw_post_data)
    content_length = len(raw_post_data)
    message = amf.AMFMessage()
    read_headers(input, message)
    read_bodies(input, message)
    return message


write_func_maps = (
        {(BooleanType,)      : 'write_boolean',},
        {(IntType, LongType, FloatType, Decimal)  : 'write_number',},
        {(StringTypes,)      : 'write_string',},
        {(ListType, TupleType, set, frozenset)  : 'write_array',},
        {(DictType,)         : 'write_object',},
        {(datetime.datetime, datetime.date) : 'write_datetime',},
        {(minidom.Document,) : 'write_xml',},
        {(NoneType,)         : 'write_null',},
        {(object,)           : 'write_custom_class',}, # default
        )

def write_data(d, output):
    amf.utils.logger().debug("amf0.write_data(%s)", repr(d))
    d = amf.utils._convert_djangotype_into_standard(d)
    for func_map in write_func_maps:
        types = func_map.keys()[0]
        if isinstance(d, types):
            func = eval(func_map.values()[0])
            if callable(func):
                func(d, output)
                return

def write_int(n, output):
    amf.utils.logger().debug("amf0.write_int(%s)", repr(n))
    output.write(struct.pack('H', socket.htons(n)))

def write_byte(b, output):
    amf.utils.logger().debug("amf0.write_byte(%s)", repr(b))
    output.write(struct.pack('B', b))

def write_long(l, output):
    amf.utils.logger().debug("amf0.write_long(%s)", repr(l))
    output.write(struct.pack('l', long(socket.htonl(l))))

def write_utf(s, output):
    s = encode_to_utf8(s)
    amf.utils.logger().debug("amf0.write_utf(%s)", repr(s))
    write_int(len(s), output)
    output.write(s)

def write_binary(b, output):
    write_int(len(b), output)
    output.write(b)

def write_long_utf(s, output):
    amf.utils.logger().debug("amf0.write_long_utf(%s)", repr(s))
    s = encode_to_utf8(s)
    write_long(len(s), output)
    output.write(s)

def encode_to_utf8(s):
    if isinstance(s, unicode):
        s = s.encode('utf_8')
    else:
        s = str(s)
    return s 

def write_string(s, output, context=None):
    amf.utils.logger().debug("amf0.write_string(%s)", repr(s))
    s = encode_to_utf8(s)
    count = len(s) 
    if (count < 65536):
        write_byte(UTF8, output)
        write_utf(s, output)
    else:
        write_byte(LONG_UTF8, output)
        write_long_utf(s, output)

def write_array(a, output, context=None):
    amf.utils.logger().debug("amf0.write_array(%s)", repr(a))
    write_byte(ARRAY, output)
    write_long(len(a), output)
    for e in a:
        write_data(e, output)

def write_double(d, output, context=None):
    amf.utils.logger().debug("amf0.write_double(%s)", repr(d))
    b = struct.pack('!d', d)
    output.write(b)    

def write_object(obj, output, context=None):
    amf.utils.logger().debug("amf0.write_object(%s)", repr(obj))
    write_byte(OBJECT, output)
    if 'iteritems' in dir(obj):
        items = obj.iteritems()
    else:
        items = obj.__dict__.iteritems()
    for key, value in items:
        write_utf(key, output)
        write_data(value, output)
    write_int(0, output)
    write_byte(END_OF_OBJECT, output)

def write_number(n, output, context=None):
    amf.utils.logger().debug("amf0.write_number(%s)", repr(n))
    if isinstance(n, Decimal): n = float(n)
    write_byte(DOUBLE, output)
    write_double(float(n), output)

def write_null(n, output, context=None):
    amf.utils.logger().debug("amf0.write_null()")
    write_byte(NULL, output)

def write_boolean(b, output, context=None):
    amf.utils.logger().debug("amf0.write_boolean(%s)", repr(b))
    write_byte(BOOL, output)
    write_byte(b, output)

def write_datetime(d, output, context=None):
    amf.utils.logger().debug("amf0.write_datetime(%s)", repr(d))
    timestamp = time.mktime(d.timetuple())
    write_byte(DATE, output)
    write_double(timestamp * 1000, output)
    write_int(0, output)

def write_xml(document, output, context=None):
    amf.utils.logger().debug("amf0.write_xml(%s)", repr(document))
    write_byte(XML, output)
    xmlstr = re.sub(r'\>(\n|\r|\r\n| |\t)*\<', '><', document.toxml().strip())
    write_long_utf(xmlstr, output)

def write_custom_class(obj, output):
    amf.utils.logger().debug("amf0.write_custom_class(%s)", repr(obj))
    write_byte(TYPED_OBJECT, output)
    type = amf.utils.get_as_type(obj)
    write_utf(type, output)
    if 'iteritems' in dir(obj): # d is a dict 
        items = obj.iteritems()
    else:
        items = obj.__dict__.iteritems()
    no_return_attrs = amf.utils.get_no_return_attrs(obj)
    for key, value in items:
        if not key in no_return_attrs:
            write_utf(key, output)
            write_data(value, output)
    write_int(0, output)
    write_byte(END_OF_OBJECT, output)

def write(message):
    output = StringIO()
    write_int(0, output)
    header_count = len(message.headers)
    write_int(header_count, output)
    for header in message.headers:
        write_utf(header['name'], output)
        write_byte(header.get('mustUnderstand', False), output) # specifies if understaning the hreader is 'required'
        content = StringIO()
        write_data(header['content'], content)
        write_long(len(content.getvalue()), output) # Length in bytes of header
        output.write(content.getvalue())
        content.close()
    body_count = len(message.bodies)
    write_int(body_count, output)
    for body in message.bodies:
        write_utf(body.target, output) # Target
        if body.response is None or body.response == '':
            body.response = 'null'
        write_utf(body.response, output) # Response
        content = StringIO()
        write_data(body.data, content) # Actual data
        write_long(len(content.getvalue()), output) # Body length in bytes
        output.write(content.getvalue())
        content.close()
    try:
        return output.getvalue()
    finally:
        output.close()

