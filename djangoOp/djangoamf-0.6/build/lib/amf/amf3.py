# vim: fileencoding=utf8
import amf, amf0, amf.utils
import re
import time
import datetime
import xml.dom.minidom as minidom
from decimal import Decimal
from types import *
try:
    set
except NameError:
    from sets import Set as set, ImmutableSet as frozenset
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

UNDEFINED     = 0x00
NULL          = 0x01
BOOLEAN_FALSE = 0x02
BOOLEAN_TRUE  = 0x03
INTEGER       = 0x04
NUMBER        = 0x05
STRING        = 0x06
XML           = 0x07
DATE          = 0x08
ARRAY         = 0x09
OBJECT        = 0x0A
LONG_XML      = 0x0B
BYTEARRAY     = 0x0C

read_func_map = {
    UNDEFINED     : None,
    NULL          : None,
    BOOLEAN_FALSE : 'read_boolean_false',
    BOOLEAN_TRUE  : 'read_boolean_true',
    INTEGER       : 'read_integer',
    NUMBER        : 'read_number',
    STRING        : 'read_string',
    DATE          : 'read_date',
    ARRAY         : 'read_array',
    OBJECT        : 'read_object',
    XML           : 'read_xml',
    LONG_XML      : 'read_xml',
    BYTEARRAY     : 'read_byte_array',
}


def read_data(input, context=None):
    amf.utils.logger().debug("read_data()")
    if not context:
        context=amf.AMFMessageBodyContext()
    if not hasattr(input, 'read'):
        input = StringIO(input)

    type = amf0.read_byte(input)
    if type == amf0.AMF3_DATA_TYPE:
        type = amf0.read_byte(input)
    amf.utils.logger().debug("AMF3 Type='%d'", type)
    if type not in read_func_map:
        amf.logger.error("Unsupported Type [type='%s']", type)
        raise Exception("Unsupported type [type='%s']" % (type,))
    func_name = read_func_map[type]
    if func_name is not None:
        func = eval(func_name)
        if callable(func):
            return func(input, context)
    return None

def read_boolean_false(input, context=None):
    return False

def read_boolean_true(input, context=None):
    return True

def read_integer(input, context=None):
    amf.utils.logger().debug("amf3.read_integer()")
    n = 0
    b = amf0.read_byte(input)
    result = 0
    while (b & 0x80) != 0 and n < 3: # Check the first bit of the byte is 1 or not
        result <<= 7
        result |= (b & 0x7F)
        b = amf0.read_byte(input)
        n += 1
    if n < 3:
        result <<= 7
        result |= b
    else:
        # Use all 8 bits from the 4th byte
        result <<= 8
        result |= b
        # Check if the integer should be negative
        if (result & 0x10000000) != 0:
            # and extend the sign bit
            #result |= 0xe0000000 # This doesn't work
            result -= 0x20000000 # TODO 
    amf.utils.logger().debug("amf3.read_integer() -- result='%s'", repr(result))
    return result

def read_number(input, context=None):
    amf.utils.logger().debug("amf3.read_number()")
    return amf0.read_double(input)

def read_string(input, context):
    amf.utils.logger().debug("amf3.read_string()")
    ref = read_integer(input)
    inline = ref & 0x01 != 0
    ref >>= 1
    if inline:
        strlen = ref
        if strlen == 0:
            return ''
        str = amf0.read_utf(input, context, strlen)
        context.add_string_reference(str)
    else:
        str = context.get_string_reference(ref)
    amf.utils.logger().debug("amf3.read_string() -- result=%s", repr(str))
    return str

def read_date(input, context):
    ref = read_integer(input)
    inline = ref & 0x01 != 0
    ref >>= 1
    if inline:
        ms = read_number(input)
        date = amf.utils.get_datetime_from_timestamp(ms)
        context.add_object_reference(date)
        return date
    else:
        return context.get_object_reference(ref)

def read_byte_array(input, context):
    amf.utils.logger().debug("amf3.read_byte_array()")
    ref = read_integer(input)
    inline = ref & 0x01 != 0
    ref >>= 1
    if inline:
        data = amf0.read_utf(input, context, ref)
        ba = amf.ByteArray(data)
        context.add_object_reference(ba)
        return ba
    else:
        return context.get_object_reference(ref)

def read_xml(input, context):
    amf.utils.logger().debug("amf3.read_xml()")
    ref = read_integer(input)
    inline = ref & 0x01 != 0
    ref >>= 1
    if inline:
        xmlStr = amf0.read_utf(input, context, ref)
        xml = minidom.parseString(xmlStr)
        context.add_object_reference(xml)
    else:
        xml = context.get_object_reference(ref)
    amf.utils.logger().debug("amf3.read_xml() -- result='%s'", xml.toxml())
    return xml

def read_array(input, context):
    amf.utils.logger().debug("amf3.read_array()")
    ref = read_integer(input)
    inline = ref & 0x01 != 0
    ref >>= 1
    if not inline:
        return context.get_object_reference(ref)

    num_of_elements = ref
    amf.utils.logger().debug("amf3.read_array() -- count='%s'", repr(num_of_elements))
    result = None
    context.add_object_reference(result)
    # The key value pairs stop when an empty string is encountered for key name.
    while True:
        key = read_data(input, context)
        amf.utils.logger().debug("amf3.read_array() -- key=%s", repr(key))
        if not key:
            break
        if not result:
            result = dict() # result is dict
        value = read_data(input, context)
        result[key] = value
    # normal array (not containing string key)
    if not result:
        result = [] # result is array
    for index in range(num_of_elements):
        elem = read_data(input, context)
        amf.utils.logger().debug("amf3.read_array() -- [%d]=%s", index, repr(elem))
        result.append(elem)
    return result

def _get_class_def(ref, input, context):
    # this second to last bit of the integer-data designates whether the object uses a reference(0) to a previously passed class-def or it is inline(1). 
    inline_class_def = ref & 0x01 != 0
    ref >>= 1
    if inline_class_def:
        # the class name is read next as string-data. 
        class_name = read_string(input, context)
        # the 3rd bit represents whether the object is Externalizable
        externalizable = ref & 0x01 != 0
        ref >>= 1
        # the 4th to last bit represents whether the object is dynamic or not
        dynamic = ref & 0x01 != 0
        ref >>= 1
        # The remaining integer-data represents the number of class members that exist
        num_of_members = ref
        member_names = []
        for i in range(num_of_members):
           member_names.append(read_string(input, context))
        class_def = {
                'type' : class_name,
                'externalizable' : externalizable,
                'dynamic' : dynamic,
                'num_of_members' : num_of_members,
                'member_names' : member_names,
                }
        amf.utils.logger().debug("Class Definition=%s", repr(class_def))
        context.add_class_def_reference(class_def)
        return class_def
    else:
        return context.get_class_def_reference(ref)

def read_object(input, context):
    ref = read_integer(input)
    inline = ref & 0x01 != 0
    ref >>= 1
    if not inline:
        return context.get_object_reference(ref)

    # inline object
    class_def = _get_class_def(ref, input, context)
    obj = dict()
    context.add_object_reference(obj)
    type = class_def['type']
    if not class_def['externalizable']:
        for name in class_def['member_names']:
            value = read_data(input, context)
            obj[name] = value

        if class_def['dynamic']:
            while True:
                key = read_string(input, context)
                if not key:
                    break
                value = read_data(input, context)
                obj[key] = value
    else:
        if type == 'flex.messaging.io.ArrayCollection' or type == 'flex.messaging.io.ObjectProxy':
            obj = read_data(input, context)
        else:
            amf.logger.error("Unsupported externalizable type [type='%s']", type)
            raise Exception("Unsupported externalizable type [type='%s']" % (type,))

    if '_explicitType' not in obj:
        obj['_explicitType'] = type
    obj = amf.utils.classcast(type, obj)
    return obj

write_func_maps = (
        {(NoneType,)         : 'write_null',},
        {(BooleanType,)      : 'write_boolean',},
        {(IntType, LongType, FloatType, Decimal)  : 'write_number',},
        {(StringTypes,)      : 'write_string',},
        {(ListType, TupleType, set, frozenset)  : 'write_array',},
        {(DictType,)         : 'write_dynamic_object',},
        {(datetime.datetime, datetime.date) : 'write_date',},
        {(minidom.Document,) : 'write_xml',},
        {(amf.ByteArray,)    : 'write_byte_array',},
        {(object,)           : 'write_object',}, # default
        )

def _write_data(d, output, context):
    amf.utils.logger().debug("amf3._write_data(%s)", repr(d))
    d = amf.utils._convert_djangotype_into_standard(d)
    for func_map in write_func_maps:
        types = func_map.keys()[0]
        if isinstance(d, types):
            func = eval(func_map.values()[0])
            if callable(func):
                func(d, output, context)
                return

def write_data(d, output=None, context=None):
    ret = False
    if not output:
        output = StringIO()
        ret = True
    if not context:
        context=amf.AMFMessageBodyContext()
    amf0.write_byte(amf0.AMF3_DATA_TYPE, output) # Type Code
    _write_data(d, output, context)
    if ret:
        try:
            return output.getvalue()
        finally:
            output.close()

def write_null(n, output, context=None):
    amf.utils.logger().debug("amf3.write_null()")
    amf0.write_byte(NULL, output) # Type Code

def write_boolean(b, output, context=None):
    if b:
        amf0.write_byte(BOOLEAN_TRUE, output) # Type Code
    else:
        amf0.write_byte(BOOLEAN_FALSE, output) # Type Code

def _write_integer(d, output, context=None):
    amf.utils.logger().debug("amf3._write_integer(%s)", repr(d))
    d &= 0x1fffffff
    if d < 0x80:
        amf0.write_byte(d, output)
    elif d < 0x4000:
        amf0.write_byte(d >> 7 & 0x7F | 0x80, output)
        amf0.write_byte(d & 0x7F, output)
    elif d < 0x200000:
        amf0.write_byte(d >> 14 & 0x7F | 0x80, output)
        amf0.write_byte(d >> 7 & 0x7F | 0x80, output)
        amf0.write_byte(d & 0x7F, output)
    else:
        amf0.write_byte(d >> 22 & 0x7F | 0x80, output)
        amf0.write_byte(d >> 15 & 0x7F | 0x80, output)
        amf0.write_byte(d >> 8 & 0x7F | 0x80, output)
        amf0.write_byte(d & 0xFF, output)

def _write_string(s, output, context):
    s = amf0.encode_to_utf8(s)
    amf.utils.logger().debug("amf3._write_string(%s)", repr(s))
    if not s:
        write_null(None, output, context)
    else:
        index = context.get_string_reference_index(s)
        if (index == -1):
            strlen = len(s)
            ref = strlen << 1
            ref |= 1
            _write_integer(ref, output)
            if strlen > 0:
                output.write(s)
                context.add_string_reference(s)
        else:
            index <<= 1
            _write_integer(index, output)

def write_string(s, output, context):
    amf0.write_byte(STRING, output) # Type Code
    _write_string(s, output, context)

def write_number(d, output, context):
    if isinstance(d, Decimal): d = float(d)
    if isinstance(d, (int, long)) and d >= -268435456 and d <= 268435455: # check valid range for 29bits
        amf0.write_byte(INTEGER, output) # Type Code
        _write_integer(d, output, context)
    else:
        amf0.write_byte(NUMBER, output) # Type Code
        amf0.write_double(d, output)

def write_date(d, output, context):
    amf.utils.logger().debug("amf3.write_date(%s)", repr(d))
    amf0.write_byte(DATE, output) # Type Code
    key = context.get_object_reference_index(d)
    if key == -1:
        ms = amf.utils.get_timestamp_from_date(d)
        _write_integer(0x01, output, context) # inline ref
        amf0.write_double(ms, output)
        context.add_object_reference(d)
    else:
        key <<= 1
        _write_integer(key, output, context)

def write_xml(document, output, context):
    xmlstr = re.sub(r'\>(\n|\r|\r\n| |\t)*\<', '><', document.toxml().strip())
    amf.utils.logger().debug("amf3.write_xml(%s)", repr(xmlstr))
    amf0.write_byte(XML, output) # Type Code
    _write_string(xmlstr, output, context)

def write_byte_array(ba, output, context):
    amf.utils.logger().debug("amf3.byte_array()")
    data = ba.data
    amf0.write_byte(BYTEARRAY, output) # Type Code
    _write_string(data, output, context)

def write_array(a, output, context):
    amf.utils.logger().debug("amf3.write_array(%s)", repr(a))
    amf0.write_byte(ARRAY, output) # Type Code
    key = context.get_object_reference_index(a)
    if key == -1:
        context.add_object_reference(a)
        count = len(a)
        ref = count << 1 | 0x01
        _write_integer(ref, output, context)
        write_null(None, output, context)
        for elem in a:
            _write_data(elem, output, context)
    else:
        key <<= 1
        _write_integer(key, output, context)

def write_dynamic_object(d, output, context):
    amf.utils.logger().debug("amf3.write_dynamice_object(%s)", repr(d))
    amf0.write_byte(OBJECT, output) # Type Code
    key = context.get_object_reference_index(d)
    if key == -1:
        context.add_object_reference(d)
        amf0.write_byte(0x0B, output) # '1011' in binary which means dynamic, inline class definition and inline object
        _write_string('', output, context) # anonymous object
        for key, value in d.iteritems():
            if not key == '_explicitType':
                _write_string(key, output, context)
                _write_data(value, output, context)
        _write_string('', output, context)
    else:
        key <<= 1
        _write_integer(key, output, context)

def write_object(d, output, context):
    amf.utils.logger().debug("amf3.write_object(%s)", repr(d))
    amf0.write_byte(OBJECT, output) # Type Code
    key = context.get_object_reference_index(d)
    ref_str = ''
    if key == -1:
        context.add_object_reference(d)
        ref_str = '1' # inline object code
        # Getting the class definition of the given object.
        class_def = amf.utils.get_class_def(d)
        class_def_key = context.get_class_def_reference_index(class_def)
        if class_def_key == -1:
            context.add_class_def_reference(class_def)
            ref_str = '001' + ref_str # '00' means Non-dynamic object and '1' means inline class-def
            ref = class_def['num_of_members']
            ref <<= 4
            ref |= int(ref_str, 2)
            _write_integer(ref, output, context)
            _write_string(class_def['type'], output, context) # class name
            for name in class_def['member_names']:
                _write_string(name, output, context) # member names
        else:
            ref_str = '0' + ref_str # referenced class-def code
            ref_str = amf.utils.to_binary(class_def_key) + ref_str
            ref = int(ref_str, 2)
            amf0.write_byte(ref, output)
        for member_name in class_def['member_names']:
            value = getattr(d, member_name, None)
            _write_data(value, output, context)
    else:
        key <<= 1
        _write_integer(key, output, context)

def _write_bodies(bodies, output):
    body_count = len(bodies)
    amf0.write_int(body_count, output)
    for body in bodies:
        context = amf.AMFMessageBodyContext()
        amf0.write_utf(body.target, output)
        if body.response is None or body.response == '':
            body.response = 'null'
        amf0.write_utf(body.response, output)

        content = StringIO()
        write_data(body.data, content, context)

        amf0.write_long(len(content.getvalue()), output) # Body length in bytes
        output.write(content.getvalue())
        content.close()

def _write_headers(headers, output):
    header_count = len(headers)
    amf0.write_int(header_count, output)
    for header in headers:
        context = amf.AMFMessageBodyContext()
        amf0.write_utf(header['name'], output)
        amf0.write_byte(header.get('mustUnderstand', False), output)
        content = StringIO()
        write_data(header['content'], content, context)
        amf0.write_long(len(content.getvalue()), output) # Length in bytes of header
        output.write(content.getvalue())
        content.close()

def write(message):
    output = StringIO()
    try:
        amf0.write_int(3, output) # version
        _write_headers(message.headers, output)
        _write_bodies(message.bodies, output)
        return output.getvalue()
    finally:
        output.close()

