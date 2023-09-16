from __future__ import print_function

import marshal
import struct
import sys
import time
from importlib.util import MAGIC_NUMBER

def _pack_uint32(val):
    """Convert integer to 32-bit little-endian bytes"""
    return struct.pack("<I", val)


def code_to_pyc_bytecode(code, mtime=0, source_size=0):
    """
    Serialise the passed code object (PyCodeObject*) to bytecode as a .pyc file

    The args mtime and source_size are inconsequential metadata in the .pyc file.
    """
    data = bytearray(MAGIC_NUMBER)

    if sys.version_info >= (3, 7):
        data.extend(_pack_uint32(0))

    data.extend(_pack_uint32(int(mtime)))

    if sys.version_info >= (3, 2):
        data.extend(_pack_uint32(source_size))

    data.extend(marshal.dumps(code))

    return data
