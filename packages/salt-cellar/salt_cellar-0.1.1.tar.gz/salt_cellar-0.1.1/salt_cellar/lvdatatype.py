import struct

from collections import namedtuple
from math import nan

from .exceptions import BlobCorruptionError

unpack_fmt = {
    'boolean': '>B',
    'dbl': '>d',
    # 'eb': '>B',  # enum not handled due to string insertion format
    # 'el': '>L',  # enum not handled due to string insertion format
    # 'ew': '>H',  # enum not handled due to string insertion format
    'ext': '>16c',  # TODO: unpack as long double instead
    'i16': '>h',
    'i32': '>i',
    'i64': '>q',
    'i8': '>b',
    's32': '>l',
    'sgl': '>f',
    'u16': '>H',
    'u32': '>I',
    'u64': '>Q',
    'u8': '>B',
}

UnpackFormat = namedtuple('UnpackFormat', ['fmt', 'len'])
unpack_format = {
    key: UnpackFormat(fmt=val, len=struct.calcsize(val))
    for key, val in unpack_fmt.items()
}


def _array(blob, data_type, indices, enum_desc=False):
    # indices = [0, 2 ,5]
    [_, data_type] = data_type.split('_')
    idx_max = max(indices)
    idx_min = min(indices)
    result = []

    # should an invalid index for the length of the array be requested,
    # return available data instead of throwing out all data
    try:
        blob_array_size = struct.unpack(">I", blob[0:4])[0]
    except struct.error:
        raise BlobCorruptionError("Array header corrupt, 4 bytes required.")

    if data_type.startswith("e"):
        # enums inserted using string format - fixed length of 4 bytes = '>L'
        cursor = 4

        # Iterate though each variable length string
        for i in range(0, idx_max + 1):
            if i in indices:
                # Extract string of interest
                string_length = struct.unpack('>L', blob[cursor : cursor + 4])[0]
                string_out = blob[cursor + 4 : cursor + 4 + string_length]

                # Extract enum integer x:description
                value, desc = string_out.split(b':')

                if enum_desc:
                    result.extend([int(value), str(desc, 'utf-8')])
                else:
                    result.append(int(value))
            else:
                string_length = struct.unpack('>L', blob[cursor : cursor + 4])[0]
                # TODO: check if idx required, if so, append result to result
                cursor += 4 + string_length
    else:
        try:
            type_spec = unpack_format[data_type]
            len_ = type_spec.len
            for idx in indices:

                try:
                    (res,) = struct.unpack(
                        type_spec.fmt, blob[4 + idx * len_ : 4 + idx * len_ + len_]
                    )
                    result.append(res)
                except struct.error:
                    # if array size is less than requested index
                    result.append(nan)

        except KeyError:
            # Converts every byte of data into the corresponding
            # 2-digit hex representation
            result = ' '.join([hex(each) for each in blob])

    return blob_array_size, result


def _scalar(value, data_type, enum_desc=False):
    if data_type == 'boolean':
        if value == 'T':
            return 1
        elif value == 'F':
            return 0
        else:
            return value

    elif data_type.startswith("e"):
        [value, desc] = value.split(':')

        if enum_desc:
            return int(value), desc
        else:
            return int(value)

    else:
        return value


def unpack(value, data_type, indices=None, enum_desc=False, size_flag=False):
    '''parses data from SQL into pythonic array

    indices of None means no array, else list of element positions
    enum_desc = include enum description in result
    size_flag = include actual blob length for arrays, None for scalar
    '''
    if indices:
        size, value = _array(value, data_type, indices, enum_desc=enum_desc)
    else:
        size = None
        value = _scalar(value, data_type, enum_desc=enum_desc)

    if size_flag:
        return size, value
    else:
        return value
