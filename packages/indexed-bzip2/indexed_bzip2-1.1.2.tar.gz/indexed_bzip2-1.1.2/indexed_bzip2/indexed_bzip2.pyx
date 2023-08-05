"""
Pyrex/C extension supporting `bx.misc.seekbzip2` (wrapping the low level
functions in `micro-bunzip.c`).
"""

from libc.stdlib cimport malloc, free
from libc.stdio cimport SEEK_SET
from libcpp.string cimport string
from libcpp.map cimport map
from libcpp cimport bool

import io
import os
import sys

ctypedef (unsigned long long int) size_t
ctypedef (long long int) lli


cdef extern from "Python.h":
    char * PyString_AsString(object)
    object PyString_FromStringAndSize(char*, int)

cdef extern from "bzip2.h":
    cppclass BZ2Reader:
        BZ2Reader(string) except +
        BZ2Reader(int) except +
        bool eof() except +
        int fileno() except +
        void close() except +
        bool closed() except +
        size_t seek(lli, int) except +
        size_t tell() except +
        size_t tellCompressed() except +
        int read(int, char*, size_t) except +
        map[size_t, size_t] blockOffsets() except +
        void setBlockOffsets(map[size_t, size_t]) except +

cdef class _IndexedBzip2File():
    cdef BZ2Reader* bz2reader

    def __cinit__(self, fileNameOrDescriptor):
        if isinstance(fileNameOrDescriptor, basestring):
            self.bz2reader = new BZ2Reader(<string>fileNameOrDescriptor.encode())
        else:
            self.bz2reader = new BZ2Reader(<int>fileNameOrDescriptor)

    def __dealloc__(self):
        del self.bz2reader

    def close(self):
        self.bz2reader.close()

    def closed(self):
        return self.bz2reader.closed()

    def fileno(self):
        return self.bz2reader.fileno()

    def read(self, size=-1):
        if size == 0 or self.bz2reader.eof():
            return b''

        cdef char* buffer
        if size > 0:
            buffer = <char*>malloc(size * sizeof(char))
            if not buffer:
                raise MemoryError()
            size = self.bz2reader.read(-1, buffer, size)
            try:
                result = <bytes> buffer[:size]
            finally:
                free(buffer)
            return result

        raise Exception("Invalid size argument")

    def seek(self, offset, whence):
        return self.bz2reader.seek(offset, whence)

    def tell(self):
        return self.bz2reader.tell()

    def tell_compressed(self):
        return self.bz2reader.tellCompressed()

    def block_offsets(self):
        return <dict>self.bz2reader.blockOffsets()

    def set_block_offsets(self, offsets):
        return self.bz2reader.setBlockOffsets(offsets)


# Extra class because cdefs are not visible from otuside but cdef class can't inherit from io.BufferedIOBase
class IndexedBzip2File(io.BufferedIOBase):
    def __init__(self, filename):
        self.bz2reader = _IndexedBzip2File(filename)
        self.name = filename
        self.mode = 'rb'

    def close(self):
        self.bz2reader.close()

    def closed(self):
        return self.bz2reader.closed()

    def fileno(self):
        return self.bz2reader.fileno()

    def seekable(self):
        return True

    def readable(self):
        return True

    def writable(self):
        return False

    def read(self, size=-1):
        if size == -1:
            result = b''
            fixedBufferSize = 1*1024*1024 # 1 MiB
            for data in iter(lambda: self.read(fixedBufferSize), b''):
                result += data
            return result
        return self.bz2reader.read(size)

    def seek(self, offset, whence=io.SEEK_SET):
        return self.bz2reader.seek(offset, whence)

    def tell(self):
        return self.bz2reader.tell()

    def tell_compressed(self):
        return self.bz2reader.tell_compressed()

    def peek(self, n=0):
        raise Exception("not supported")

    def read1(self, size=-1):
        raise Exception("not supported")

    def readinto(self, b):
        raise Exception("not supported")

    def readline(self, size=-1):
        raise Exception("not supported")

    def readlines(self, size=-1):
        raise Exception("not supported")

    def write(self, data):
        raise Exception("not supported")

    def writelines(self, seq):
        raise Exception("not supported")

    def block_offsets(self):
        return self.bz2reader.block_offsets()

    def set_block_offsets(self, offsets):
        return self.bz2reader.set_block_offsets(offsets)

__version__ = '1.1.2'
