# cython: language_level=3, boundscheck=False
import numpy as np
cimport numpy as np
from sys import byteorder
from libc.stdint cimport uint16_t, uint32_t, uint64_t
from libc.stdio cimport printf
from cpython.mem cimport PyMem_Malloc, PyMem_Free
from cpython.bytes cimport PyBytes_AsString
from libc.string cimport memcpy
cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)
def sorted_data_read(bytes tmp, unsigned short bit_count,
        unsigned short signal_data_type, str record_format, unsigned long long number_of_records,
        unsigned long record_byte_size, unsigned char bit_offset,
        unsigned long pos_byte_beg, unsigned long n_bytes, array):
    """dataRead function to read in cython a channel from a byte stream

    Parameters
    ------------
    tmp : bytes
        byte stream
    bit_count : unsigned short
        number of bit taken by the channel in the record
    signal_data_type : unsigned short
        int to describe data type
    record_format : string
        basic numpy dtype description of data type, used to create
        returned numpy ndarray
    number_of_records : unsigned long long
        number of records in byte stream
    record_byte_size : unsigned long
        number of bytes taken by one record repeated in byte stream
    bit_offset : unsigned char
        bit offset of data in C aligned bytes
    pos_byte_beg : unsigned long
        beginning byte position of channel in record
    n_bytes : unsigned long
        bytes length of channel in record
    array : boolean
        reads an array, not a vector

    Returns
    -------
    ndarray of type record_format with number_of_records records.
    Byte order is swapped if necessary to match machine byte order before bits offset and masking
    """
    cdef char* bit_stream = PyBytes_AsString(tmp)
    if not array:
        if 'V' in record_format or 'S' in record_format or record_format is None:
            return read_byte(bit_stream, record_format, number_of_records,
                                record_byte_size, pos_byte_beg, n_bytes, bit_count, bit_offset)
        elif signal_data_type in (4, 5) and n_bytes == 4:  # float
            if (byteorder == 'little' and signal_data_type == 4) or \
                    (byteorder == 'big' and signal_data_type == 5):
                return read_float(bit_stream, record_format, number_of_records,
                                     record_byte_size, pos_byte_beg, 0)
            else: #  swap bytes
                return read_float(bit_stream, record_format, number_of_records,
                                     record_byte_size, pos_byte_beg, 1)
        elif signal_data_type in (4, 5) and n_bytes == 8:  # double
            if (byteorder == 'little' and signal_data_type == 4) or \
                    (byteorder == 'big' and signal_data_type == 5):
                return read_double(bit_stream, record_format, number_of_records,
                                      record_byte_size, pos_byte_beg, 0)
            else: #  swap bytes
                return read_double(bit_stream, record_format, number_of_records,
                                      record_byte_size, pos_byte_beg, 1)
        elif signal_data_type in (4, 5) and n_bytes == 2:  # half precision
            if (byteorder == 'little' and signal_data_type == 4) or \
                    (byteorder == 'big' and signal_data_type == 5):
                return read_half(bit_stream, record_format, number_of_records,
                                      record_byte_size, pos_byte_beg, 0)
            else: #  swap bytes
                return read_half(bit_stream, record_format, number_of_records,
                                      record_byte_size, pos_byte_beg, 1)
        elif signal_data_type in (0, 1, 13) and n_bytes == 1:  # unsigned char
            return read_unsigned_char(bit_stream, record_format, number_of_records,
                                 record_byte_size, pos_byte_beg, bit_count, bit_offset)
        elif signal_data_type in (2, 3) and n_bytes == 1:  # signed char
            return read_signed_char(bit_stream, record_format, number_of_records,
                                record_byte_size, pos_byte_beg, bit_count, bit_offset)
        elif signal_data_type in (0, 1, 13, 14) and n_bytes <= 2:  # unsigned short
            if (byteorder == 'little' and signal_data_type == 0) or \
                    (byteorder == 'big' and signal_data_type == 1):
                return read_unsigned_short(bit_stream, record_format, number_of_records,
                                      record_byte_size, pos_byte_beg, bit_count, bit_offset, 0)
            else: #  swap bytes
                return read_unsigned_short(bit_stream, record_format, number_of_records,
                                      record_byte_size, pos_byte_beg, bit_count, bit_offset, 1)
        elif signal_data_type in (2, 3) and n_bytes <= 2:  # signed short
            if (byteorder == 'little' and signal_data_type == 2) or \
                    (byteorder == 'big' and signal_data_type == 3):
                return read_signed_short(bit_stream, record_format, number_of_records,
                                     record_byte_size, pos_byte_beg, bit_count, bit_offset, 0)
            else: #  swap bytes
                return read_signed_short(bit_stream, record_format, number_of_records,
                                     record_byte_size, pos_byte_beg, bit_count, bit_offset, 1)
        elif signal_data_type in (0, 1, 14) and n_bytes <= 4:  # unsigned int
            if (byteorder == 'little' and signal_data_type == 0) or \
                    (byteorder == 'big' and signal_data_type == 1):
                return read_unsigned_int(bit_stream, record_format, number_of_records,
                                    record_byte_size, pos_byte_beg, bit_count, bit_offset, n_bytes, 0)
            else: #  swap bytes
                return read_unsigned_int(bit_stream, record_format, number_of_records,
                                    record_byte_size, pos_byte_beg, bit_count, bit_offset, n_bytes, 1)
        elif signal_data_type in (2, 3) and n_bytes <= 4:  # signed int
            if (byteorder == 'little' and signal_data_type == 2) or \
                    (byteorder == 'big' and signal_data_type == 3):
                return read_signed_int(bit_stream, record_format, number_of_records,
                                   record_byte_size, pos_byte_beg, bit_count, bit_offset, n_bytes, 0)
            else: #  swap bytes
                return read_signed_int(bit_stream, record_format, number_of_records,
                                   record_byte_size, pos_byte_beg, bit_count, bit_offset, n_bytes, 1)
        elif signal_data_type in (0, 1) and n_bytes <= 8:  # unsigned long long
            if (byteorder == 'little' and signal_data_type == 0) or \
                    (byteorder == 'big' and signal_data_type == 1):
                return read_unsigned_longlong(bit_stream, record_format, number_of_records,
                                         record_byte_size, pos_byte_beg, bit_count, bit_offset, n_bytes, 0)
            else: #  swap bytes
                return read_unsigned_longlong(bit_stream, record_format, number_of_records,
                                         record_byte_size, pos_byte_beg, bit_count, bit_offset, n_bytes, 1)
        elif signal_data_type in (2, 3) and n_bytes <= 8:  # signed long long
            if (byteorder == 'little' and signal_data_type == 2) or \
                    (byteorder == 'big' and signal_data_type == 3):
                return read_signed_longlong(bit_stream, record_format, number_of_records,
                                        record_byte_size, pos_byte_beg, bit_count, bit_offset, n_bytes, 0)
            else: #  swap bytes
                return read_signed_longlong(bit_stream, record_format, number_of_records,
                                        record_byte_size, pos_byte_beg, bit_count, bit_offset, n_bytes, 1)
        elif signal_data_type in (15, 16):  # complex
            if (byteorder == 'little' and signal_data_type == 0) or \
                    (byteorder == 'big' and signal_data_type == 1):
                swap_flag = 0
            else: #  swap bytes
                swap_flag = 1
            if n_bytes == 16:
                return read_cdouble(bit_stream, record_format, number_of_records,
                                      record_byte_size, pos_byte_beg, 0)
            elif n_bytes == 8:
                return read_cfloat(bit_stream, record_format, number_of_records,
                                      record_byte_size, pos_byte_beg, 0)
            elif n_bytes == 4:
                return read_chalf(bit_stream, record_format, number_of_records,
                                      record_byte_size, pos_byte_beg, 0)
        else:
            return read_byte(bit_stream, record_format, number_of_records,
                                record_byte_size, pos_byte_beg, n_bytes, bit_count, bit_offset)
    else: # array
        if (byteorder == 'little' and signal_data_type in (0, 2, 4)) or \
                    (byteorder == 'big' and signal_data_type in (1, 3, 5)):
            return read_array(bit_stream, record_format, number_of_records,
                                 record_byte_size, pos_byte_beg, n_bytes, bit_count, bit_offset, 0)
        else: #  swap bytes
            return read_array(bit_stream, record_format, number_of_records,
                                 record_byte_size, pos_byte_beg, n_bytes, bit_count, bit_offset, 1)

cdef inline read_half(const char* bit_stream, str record_format, unsigned long long number_of_records,
        unsigned long record_byte_size, unsigned long pos_byte_beg, unsigned char swap):
    cdef uint16_t[:] buf = np.empty(number_of_records, dtype=np.uint16)
    cdef unsigned long long i
    cdef uint16_t temp_uint16 = 0  # using uint16 because float16_t is not existing
    for i in range(number_of_records):
        memcpy(&temp_uint16, &bit_stream[pos_byte_beg + record_byte_size * i], 2)
        buf[i] = temp_uint16
    if swap == 0:
        return np.asarray(buf).view(dtype=np.float16)
    else:
        return np.asarray(buf).view(dtype=np.float16).byteswap()

cdef inline read_chalf(const char* bit_stream, str record_format, unsigned long long number_of_records,
        unsigned long record_byte_size, unsigned long pos_byte_beg, unsigned char swap):
    cdef uint64_t[:] buf = np.empty(number_of_records, dtype=np.uint32)  # complex_32 does not exist in numpy
    cdef unsigned long long i
    cdef uint16_t temp16_real = 0
    cdef uint16_t temp16_img = 0
    for i in range(number_of_records):
        memcpy(&temp16_real, &bit_stream[pos_byte_beg + record_byte_size * i], 2)
        memcpy(&temp16_img, &bit_stream[pos_byte_beg + record_byte_size * i], 2)
        buf[i] = <uint32_t>temp16_real<<32 | <uint32_t>temp16_img
    if swap == 0:
        return np.asarray(buf).view(dtype=np.complex_64)  # returning single instead of half precision complex
    else:
        return np.asarray(buf).view(dtype=np.complex_64).byteswap()

cdef inline read_float(const char* bit_stream, str record_format, unsigned long long number_of_records,
        unsigned long record_byte_size, unsigned long pos_byte_beg, unsigned char swap):
    cdef np.ndarray[np.float32_t] buf = np.empty(number_of_records, dtype=record_format)  # return numpy array
    cdef unsigned long long i
    cdef float temp_float = 0
    for i in range(number_of_records):
        memcpy(&temp_float, &bit_stream[pos_byte_beg + record_byte_size * i], 4)
        buf[i] = temp_float
    if swap == 0:
        return buf
    else:
        return buf.byteswap()

cdef inline read_cfloat(const char* bit_stream, str record_format, unsigned long long number_of_records,
        unsigned long record_byte_size, unsigned long pos_byte_beg, unsigned char swap):
    cdef np.ndarray[np.complex64_t] buf = np.empty(number_of_records, dtype=record_format)  # return numpy array
    cdef unsigned long long i
    cdef float complex temp_cfloat = 0
    for i in range(number_of_records):
        memcpy(&temp_cfloat, &bit_stream[pos_byte_beg + record_byte_size * i], 8)
        buf[i] = temp_cfloat
    if swap == 0:
        return buf
    else:
        return buf.byteswap()

cdef inline read_double(const char* bit_stream, str record_format, unsigned long long number_of_records,
        unsigned long record_byte_size, unsigned long pos_byte_beg, unsigned char swap):
    cdef np.ndarray[np.float64_t] buf = np.empty(number_of_records, dtype=record_format)  # return numpy array
    cdef unsigned long long i
    cdef double temp_double = 0
    for i in range(number_of_records):
        memcpy(&temp_double, &bit_stream[pos_byte_beg + record_byte_size * i], 8)
        buf[i] = temp_double
    if swap == 0:
        return buf
    else:
        return buf.byteswap()

cdef inline read_cdouble(const char* bit_stream, str record_format, unsigned long long number_of_records,
        unsigned long record_byte_size, unsigned long pos_byte_beg, unsigned char swap):
    cdef np.ndarray[np.complex128_t] buf = np.empty(number_of_records, dtype=record_format)  # return numpy array
    cdef unsigned long long i
    cdef double complex temp_cdouble = 0
    for i in range(number_of_records):
        memcpy(&temp_cdouble, &bit_stream[pos_byte_beg + record_byte_size * i], 16)
        buf[i] = temp_cdouble
    if swap == 0:
        return buf
    else:
        return buf.byteswap()

cdef inline read_unsigned_char(const char* bit_stream, str record_format, unsigned long long number_of_records,
        unsigned long record_byte_size, unsigned long pos_byte_beg,
        unsigned long bit_count, unsigned char bit_offset):
    cdef np.ndarray[np.uint8_t] buf = np.empty(number_of_records, dtype=record_format)  # return numpy array
    cdef unsigned long long i
    cdef unsigned char mask = ((1 << bit_count) - 1)
    cdef unsigned char temp1byte = 0
    if bit_count == 8:
        for i in range(number_of_records):
            memcpy(&temp1byte, &bit_stream[pos_byte_beg + record_byte_size * i], 1)
            buf[i] = temp1byte
    else:
        for i in range(number_of_records):
            memcpy(&temp1byte, &bit_stream[pos_byte_beg + record_byte_size * i], 1)
            # right shift 
            if bit_offset > 0:
                temp1byte = temp1byte >> bit_offset
            # mask left part
            temp1byte &= mask
            buf[i] = temp1byte
    return buf

cdef inline read_signed_char(const char* bit_stream, str record_format, unsigned long long number_of_records,
        unsigned long record_byte_size, unsigned long pos_byte_beg,
        unsigned long bit_count, unsigned char bit_offset):
    cdef np.ndarray[np.int8_t] buf = np.empty(number_of_records, dtype=record_format)  # return numpy array
    cdef unsigned long long i
    cdef unsigned char mask = ((1 << bit_count) - 1)
    cdef char temp1byte = 0
    cdef unsigned char sign_bit = 0
    cdef unsigned char sign_bit_mask = (1 << (bit_count-1))
    cdef unsigned char sign_extend = ((1 << (8 - bit_count)) - 1) << bit_count
    if bit_count == 8:
        for i in range(number_of_records):
            memcpy(&temp1byte, &bit_stream[pos_byte_beg + record_byte_size * i], 1)
            buf[i] = temp1byte
    else:
        for i in range(number_of_records):
            memcpy(&temp1byte, &bit_stream[pos_byte_beg + record_byte_size * i], 1)
            # right shift 
            if bit_offset > 0:
                temp1byte = temp1byte >> bit_offset
            # mask left part
            temp1byte &= mask
            sign_bit = temp1byte & sign_bit_mask
            if sign_bit: #  negative value, sign extend
                temp1byte |= sign_extend
            buf[i] = temp1byte
    return buf

cdef inline read_unsigned_short(const char* bit_stream, str record_format, unsigned long long number_of_records,
        unsigned long record_byte_size, unsigned long pos_byte_beg,
        unsigned long bit_count, unsigned char bit_offset, unsigned char swap):
    cdef np.ndarray[np.uint16_t] buf = np.empty(number_of_records, dtype=record_format)  # return numpy array
    cdef unsigned long long i
    cdef unsigned short mask = ((1 << bit_count) - 1)
    cdef unsigned short temp2byte = 0
    cdef unsigned char temp[2]
    if bit_count == 16:
        for i in range(number_of_records):
            memcpy(&temp2byte, &bit_stream[pos_byte_beg + record_byte_size * i], 2)
            buf[i] = temp2byte
        if swap == 0:
            return buf
        else:
            return buf.byteswap()
    else:
        if swap == 0:
            for i in range(number_of_records):
                memcpy(&temp2byte, &bit_stream[pos_byte_beg + record_byte_size * i], 2)
                # right shift
                if bit_offset > 0:
                    temp2byte = temp2byte >> bit_offset
                # mask left part
                if bit_count < 16:
                    temp2byte &= mask
                buf[i] = temp2byte
        else:
            for i in range(number_of_records):
                memcpy(&temp, &bit_stream[pos_byte_beg + record_byte_size * i], 2)
                temp2byte = temp[0]<<8 | temp[1]  #  swap bytes
                # right shift
                if bit_offset > 0:
                    temp2byte = temp2byte >> bit_offset
                # mask left part
                if bit_count < 16:
                    temp2byte &= mask
                buf[i] = temp2byte
        return buf

cdef inline read_signed_short(const char* bit_stream, str record_format, unsigned long long number_of_records,
        unsigned long record_byte_size, unsigned long pos_byte_beg,
        unsigned long bit_count, unsigned char bit_offset, unsigned char swap):
    cdef np.ndarray[np.int16_t] buf = np.empty(number_of_records, dtype=record_format)  # return numpy array
    cdef unsigned long long i
    cdef unsigned short mask = ((1 << bit_count) - 1)
    cdef short temp2byte = 0
    cdef unsigned short sign_bit = 0
    cdef unsigned short sign_bit_mask = (1 << (bit_count-1))
    cdef unsigned short sign_extend = ((1 << (16 - bit_count)) - 1) << bit_count
    cdef unsigned char temp[2]
    if bit_count == 16:
        for i in range(number_of_records):
            memcpy(&temp2byte, &bit_stream[pos_byte_beg + record_byte_size * i], 2)
            buf[i] = temp2byte
        if swap == 0:
            return buf
        else:
            return buf.byteswap()
    else:
        if swap == 0:
            for i in range(number_of_records):
                memcpy(&temp2byte, &bit_stream[pos_byte_beg + record_byte_size * i], 2)
                # right shift
                if bit_offset > 0:
                    temp2byte = temp2byte >> bit_offset
                # mask left part
                temp2byte &= mask
                sign_bit = temp2byte & sign_bit_mask
                if sign_bit: #  negative value, sign extend
                    temp2byte |= sign_extend
                buf[i] = temp2byte
        else:
            for i in range(number_of_records):
                memcpy(&temp, &bit_stream[pos_byte_beg + record_byte_size * i], 2)
                temp2byte = temp[0]<<8 | temp[1]  #  swap bytes
                # right shift
                if bit_offset > 0:
                    temp2byte = temp2byte >> bit_offset
                # mask left part
                temp2byte &= mask
                sign_bit = temp2byte & sign_bit_mask
                if sign_bit: #  negative value, sign extend
                    temp2byte |= sign_extend
                buf[i] = temp2byte
        return buf

cdef inline read_unsigned_int(const char* bit_stream, str record_format, unsigned long long number_of_records,
        unsigned long record_byte_size, unsigned long pos_byte_beg,
        unsigned long bit_count, unsigned char bit_offset, unsigned long n_bytes, unsigned char swap):
    cdef np.ndarray[np.uint32_t] buf = np.empty(number_of_records, dtype=record_format)  # return numpy array
    cdef unsigned long long i
    cdef unsigned int mask = ((1 << bit_count) - 1)
    cdef unsigned int temp4byte = 0
    cdef unsigned char temp4[4]
    cdef unsigned char temp3[3]
    if bit_count == 32:
        for i in range(number_of_records):
            memcpy(&temp4byte, &bit_stream[pos_byte_beg + record_byte_size * i], 4)
            buf[i] = temp4byte
        if swap == 0:
            return buf
        else:
            return buf.byteswap()
    elif n_bytes == 4:
        if swap == 0:
            for i in range(number_of_records):
                memcpy(&temp4byte, &bit_stream[pos_byte_beg + record_byte_size * i], n_bytes)
                # right shift
                if bit_offset > 0:
                    temp4byte = temp4byte >> bit_offset
                # mask left part
                if bit_count < 32:
                    temp4byte &= mask
                buf[i] = temp4byte
        else:
            for i in range(number_of_records):
                memcpy(&temp4, &bit_stream[pos_byte_beg + record_byte_size * i], n_bytes)
                temp4byte = temp4[0]<<24 | temp4[1]<<16 | temp4[2]<<8 | temp4[3]  #  swap bytes
                # right shift
                if bit_offset > 0:
                    temp4byte = temp4byte >> bit_offset
                # mask left part
                if bit_count < 32:
                    temp4byte &= mask
                buf[i] = temp4byte
        return buf
    else:  # on 3 bytes
        if swap == 0:
            for i in range(number_of_records):
                memcpy(&temp4byte, &bit_stream[pos_byte_beg + record_byte_size * i], n_bytes)
                # right shift 
                if bit_offset > 0:
                    temp4byte = temp4byte >> bit_offset
                # mask left part
                if bit_count < 24:
                    temp4byte &= mask
                buf[i] = temp4byte
        else:
            for i in range(number_of_records):
                memcpy(&temp3, &bit_stream[pos_byte_beg + record_byte_size * i], n_bytes)
                temp4byte = temp3[0]<<16 | temp3[1]<<8 | temp3[2]  #  swap bytes
                # right shift 
                if bit_offset > 0:
                    temp4byte = temp4byte >> bit_offset
                # mask left part
                if bit_count < 24:
                    temp4byte &= mask
                buf[i] = temp4byte
        return buf


cdef inline read_signed_int(const char* bit_stream, str record_format, unsigned long long number_of_records,
        unsigned long record_byte_size, unsigned long pos_byte_beg,
        unsigned long bit_count, unsigned char bit_offset, unsigned long n_bytes, unsigned char swap):
    cdef np.ndarray[np.int32_t] buf = np.empty(number_of_records, dtype=record_format)  # return numpy array
    cdef unsigned long long i
    cdef unsigned int mask = ((1 << bit_count) - 1)
    cdef int temp4byte = 0
    cdef unsigned int sign_bit = 0
    cdef unsigned int sign_bit_mask = (1 << (bit_count-1))
    cdef unsigned int sign_extend = ((1 << (32 - bit_count)) - 1) << bit_count
    cdef unsigned char temp4[4]
    cdef unsigned char temp3[3]
    if bit_count == 32:
        for i in range(number_of_records):
            memcpy(&temp4byte, &bit_stream[pos_byte_beg + record_byte_size * i], 4)
            buf[i] = temp4byte
        if swap == 0:
            return buf
        else:
            return buf.byteswap()
    elif n_bytes == 4:
        if swap == 0:
            for i in range(number_of_records):
                memcpy(&temp4byte, &bit_stream[pos_byte_beg + record_byte_size * i], n_bytes)
                # right shift
                if bit_offset > 0:
                    temp4byte = temp4byte >> bit_offset
                # mask left part
                if bit_count < 32:
                    temp4byte &= mask
                sign_bit = temp4byte & sign_bit_mask # assumes return in little endian, to be reviewed
                if sign_bit: #  negative value, sign extend
                    temp4byte |= sign_extend
                buf[i] = temp4byte
        else:
            for i in range(number_of_records):
                memcpy(&temp4, &bit_stream[pos_byte_beg + record_byte_size * i], n_bytes)
                temp4byte = temp4[0]<<24 | temp4[1]<<16 | temp4[2]<<8 | temp4[3]  #  swap bytes
                # right shift
                if bit_offset > 0:
                    temp4byte = temp4byte >> bit_offset
                # mask left part
                if bit_count < 32:
                    temp4byte &= mask
                sign_bit = temp4byte & sign_bit_mask # assumes return in little endian, to be reviewed
                if sign_bit: #  negative value, sign extend
                    temp4byte |= sign_extend
                buf[i] = temp4byte
        return buf
    else:  # on 3 bytes
        if swap == 0:
            for i in range(number_of_records):
                memcpy(&temp4byte, &bit_stream[pos_byte_beg + record_byte_size * i], n_bytes)
                # right shift 
                if bit_offset > 0:
                    temp4byte = temp4byte >> bit_offset
                # mask left part
                if bit_count < 24:
                    temp4byte &= mask
                sign_bit = temp4byte & sign_bit_mask # assumes return in little endian, to be reviewed
                if sign_bit: #  negative value, sign extend
                    temp4byte |= sign_extend
                buf[i] = temp4byte
        else:
            for i in range(number_of_records):
                memcpy(&temp3, &bit_stream[pos_byte_beg + record_byte_size * i], n_bytes)
                temp4byte = temp3[0]<<16 | temp3[1]<<8 | temp3[2]  #  swap bytes
                # right shift 
                if bit_offset > 0:
                    temp4byte = temp4byte >> bit_offset
                # mask left part
                if bit_count < 24:
                    temp4byte &= mask
                sign_bit = temp4byte & sign_bit_mask # assumes return in little endian, to be reviewed
                if sign_bit: #  negative value, sign extend
                    temp4byte |= sign_extend
                buf[i] = temp4byte
        return buf

cdef inline read_unsigned_longlong(const char* bit_stream, str record_format, unsigned long long number_of_records,
        unsigned long record_byte_size, unsigned long pos_byte_beg,
        unsigned long bit_count, unsigned char bit_offset, unsigned long n_bytes, unsigned char swap):
    cdef np.ndarray[np.uint64_t] buf = np.empty(number_of_records, dtype=record_format)  # return numpy array
    cdef unsigned long long i
    cdef unsigned long long mask = ((1 << bit_count) - 1)
    cdef unsigned long long temp8byte = 0
    cdef unsigned char temp8[8]
    cdef unsigned char temp7[7]
    cdef unsigned char temp6[6]
    cdef unsigned char temp5[5]
    if bit_count == 64:
        for i in range(number_of_records):
            memcpy(&temp8byte, &bit_stream[pos_byte_beg + record_byte_size * i], n_bytes)
            buf[i] = temp8byte
        if swap == 0:
            return buf
        else:
            return buf.byteswap()
    elif n_bytes == 8:
        if swap == 0:
            for i in range(number_of_records):
                memcpy(&temp8byte, &bit_stream[pos_byte_beg + record_byte_size * i], n_bytes)
                # right shift
                if bit_offset > 0:
                    temp8byte = temp8byte >> bit_offset
                # mask left part
                if bit_count < 64:
                    temp8byte &= mask
                buf[i] = temp8byte
        else:
            for i in range(number_of_records):
                memcpy(&temp8, &bit_stream[pos_byte_beg + record_byte_size * i], n_bytes)
                temp8byte = temp8[0]<<56 | temp8[1]<<48 | temp8[2]<<40 | temp8[3]<<32 | \
                            temp8[4]<<24 | temp8[5]<<16 | temp8[6]<<8 | temp8[7] #  swap bytes
                # right shift
                if bit_offset > 0:
                    temp8byte = temp8byte >> bit_offset
                # mask left part
                if bit_count < 64:
                    temp8byte &= mask
                buf[i] = temp8byte
    elif n_bytes == 7:
        if swap == 0:
            for i in range(number_of_records):
                memcpy(&temp8byte, &bit_stream[pos_byte_beg + record_byte_size * i], n_bytes)
                # right shift
                if bit_offset > 0:
                    temp8byte = temp8byte >> bit_offset
                # mask left part
                if bit_count < 56:
                    temp8byte &= mask
                buf[i] = temp8byte
        else:
            for i in range(number_of_records):
                memcpy(&temp7, &bit_stream[pos_byte_beg + record_byte_size * i], n_bytes)
                temp8byte = temp7[0]<<48 | temp7[1]<<40 | temp7[2]<<32 | \
                            temp7[3]<<24 | temp7[4]<<16 | temp7[5]<<8 | temp7[6] #  swap bytes
                # right shift
                if bit_offset > 0:
                    temp8byte = temp8byte >> bit_offset
                # mask left part
                if bit_count < 56:
                    temp8byte &= mask
                buf[i] = temp8byte
    elif n_bytes == 6:
        if swap == 0:
            for i in range(number_of_records):
                memcpy(&temp8byte, &bit_stream[pos_byte_beg + record_byte_size * i], n_bytes)
                # right shift
                if bit_offset > 0:
                    temp8byte = temp8byte >> bit_offset
                # mask left part
                if bit_count < 48:
                    temp8byte &= mask
                buf[i] = temp8byte
        else:
            for i in range(number_of_records):
                memcpy(&temp6, &bit_stream[pos_byte_beg + record_byte_size * i], n_bytes)
                temp8byte = temp6[0]<<40 | temp6[1]<<32 | temp6[2]<<24 | \
                            temp6[3]<<16 | temp6[4]<<8 | temp6[5] #  swap bytes
                # right shift
                if bit_offset > 0:
                    temp8byte = temp8byte >> bit_offset
                # mask left part
                if bit_count < 48:
                    temp8byte &= mask
                buf[i] = temp8byte
    elif n_bytes == 5:
        if swap == 0:
            for i in range(number_of_records):
                memcpy(&temp8byte, &bit_stream[pos_byte_beg + record_byte_size * i], n_bytes)
                # right shift
                if bit_offset > 0:
                    temp8byte = temp8byte >> bit_offset
                # mask left part
                if bit_count < 32:
                    temp8byte &= mask
                buf[i] = temp8byte
        else:
            for i in range(number_of_records):
                memcpy(&temp5, &bit_stream[pos_byte_beg + record_byte_size * i], n_bytes)
                temp8byte = temp5[0]<<32 | temp5[1]<<24 | \
                            temp5[2]<<16 | temp5[3]<<8 | temp5[4] #  swap bytes
                # right shift
                if bit_offset > 0:
                    temp8byte = temp8byte >> bit_offset
                # mask left part
                if bit_count < 32:
                    temp8byte &= mask
                buf[i] = temp8byte
    return buf

cdef inline read_signed_longlong(const char* bit_stream, str record_format, unsigned long long number_of_records,
        unsigned long record_byte_size, unsigned long pos_byte_beg,
        unsigned long bit_count, unsigned char bit_offset, unsigned long n_bytes, unsigned char swap):
    cdef np.ndarray[np.int64_t] buf = np.empty(number_of_records, dtype=record_format)  # return numpy array
    cdef unsigned long long i
    cdef unsigned long long mask = ((1 << bit_count) - 1)
    cdef long long temp8byte = 0
    cdef unsigned long sign_bit = 0
    cdef unsigned long long sign_bit_mask = (1 << (bit_count-1))
    cdef unsigned long long sign_extend = ((1 << (64 - bit_count)) - 1) << bit_count
    cdef unsigned char temp8[8]
    cdef unsigned char temp7[7]
    cdef unsigned char temp6[6]
    cdef unsigned char temp5[5]
    if bit_count == 64:
        for i in range(number_of_records):
            memcpy(&temp8byte, &bit_stream[pos_byte_beg + record_byte_size * i], n_bytes)
            buf[i] = temp8byte
        if swap == 0:
            return buf
        else:
            return buf.byteswap()
    elif n_bytes == 8:
        if swap == 0:
            for i in range(number_of_records):
                memcpy(&temp8byte, &bit_stream[pos_byte_beg + record_byte_size * i], n_bytes)
                # right shift
                if bit_offset > 0:
                    temp8byte = temp8byte >> bit_offset
                # mask left part
                if bit_count < 64:
                    temp8byte &= mask
                sign_bit = temp8byte & sign_bit_mask
                if sign_bit: #  negative value, sign extend
                    temp8byte |= sign_extend
                buf[i] = temp8byte
        else:
            for i in range(number_of_records):
                memcpy(&temp8, &bit_stream[pos_byte_beg + record_byte_size * i], n_bytes)
                temp8byte = temp8[0]<<56 | temp8[1]<<48 | temp8[2]<<40 | temp8[3]<<32 | \
                            temp8[4]<<24 | temp8[5]<<16 | temp8[6]<<8 | temp8[7] #  swap bytes
                # right shift
                if bit_offset > 0:
                    temp8byte = temp8byte >> bit_offset
                # mask left part
                if bit_count < 64:
                    temp8byte &= mask
                sign_bit = temp8byte & sign_bit_mask
                if sign_bit: #  negative value, sign extend
                    temp8byte |= sign_extend
                buf[i] = temp8byte
    elif n_bytes == 7:
        if swap == 0:
            for i in range(number_of_records):
                memcpy(&temp8byte, &bit_stream[pos_byte_beg + record_byte_size * i], n_bytes)
                # right shift
                if bit_offset > 0:
                    temp8byte = temp8byte >> bit_offset
                # mask left part
                if bit_count < 56:
                    temp8byte &= mask
                sign_bit = temp8byte & sign_bit_mask
                if sign_bit: #  negative value, sign extend
                    temp8byte |= sign_extend
                buf[i] = temp8byte
        else:
            for i in range(number_of_records):
                memcpy(&temp7, &bit_stream[pos_byte_beg + record_byte_size * i], n_bytes)
                temp8byte = temp7[0]<<48 | temp7[1]<<40 | temp7[2]<<32 | \
                            temp7[3]<<24 | temp7[4]<<16 | temp7[5]<<8 | temp7[6] #  swap bytes
                # right shift
                if bit_offset > 0:
                    temp8byte = temp8byte >> bit_offset
                # mask left part
                if bit_count < 56:
                    temp8byte &= mask
                sign_bit = temp8byte & sign_bit_mask
                if sign_bit: #  negative value, sign extend
                    temp8byte |= sign_extend
                buf[i] = temp8byte
    elif n_bytes == 6:
        if swap == 0:
            for i in range(number_of_records):
                memcpy(&temp8byte, &bit_stream[pos_byte_beg + record_byte_size * i], n_bytes)
                # right shift
                if bit_offset > 0:
                    temp8byte = temp8byte >> bit_offset
                # mask left part
                if bit_count < 48:
                    temp8byte &= mask
                sign_bit = temp8byte & sign_bit_mask
                if sign_bit: #  negative value, sign extend
                    temp8byte |= sign_extend
                buf[i] = temp8byte
        else:
            for i in range(number_of_records):
                memcpy(&temp6, &bit_stream[pos_byte_beg + record_byte_size * i], n_bytes)
                temp8byte = temp6[0]<<40 | temp6[1]<<32 | temp6[2]<<24 | \
                            temp6[3]<<16 | temp6[4]<<8 | temp6[5] #  swap bytes
                # right shift
                if bit_offset > 0:
                    temp8byte = temp8byte >> bit_offset
                # mask left part
                if bit_count < 48:
                    temp8byte &= mask
                sign_bit = temp8byte & sign_bit_mask
                if sign_bit: #  negative value, sign extend
                    temp8byte |= sign_extend
                buf[i] = temp8byte
    elif n_bytes == 5:
        if swap == 0:
            for i in range(number_of_records):
                memcpy(&temp8byte, &bit_stream[pos_byte_beg + record_byte_size * i], n_bytes)
                # right shift
                if bit_offset > 0:
                    temp8byte = temp8byte >> bit_offset
                # mask left part
                if bit_count < 40:
                    temp8byte &= mask
                sign_bit = temp8byte & sign_bit_mask
                if sign_bit: #  negative value, sign extend
                    temp8byte |= sign_extend
                buf[i] = temp8byte
        else:
            for i in range(number_of_records):
                memcpy(&temp5, &bit_stream[pos_byte_beg + record_byte_size * i], n_bytes)
                temp8byte = temp5[0]<<32 | temp5[1]<<24 | \
                            temp5[2]<<16 | temp5[3]<<8 | temp5[4] #  swap bytes
                # right shift
                if bit_offset > 0:
                    temp8byte = temp8byte >> bit_offset
                # mask left part
                if bit_count < 40:
                    temp8byte &= mask
                sign_bit = temp8byte & sign_bit_mask
                if sign_bit: #  negative value, sign extend
                    temp8byte |= sign_extend
                buf[i] = temp8byte
    return buf

cdef inline read_byte(const char* bit_stream, str record_format, unsigned long long number_of_records,
        unsigned long record_byte_size, unsigned long pos_byte_beg, unsigned long n_bytes,
        unsigned long bit_count, unsigned char bit_offset):
    cdef np.ndarray buf = np.empty(number_of_records, dtype=record_format)  # return numpy array
    cdef unsigned long long i
    cdef unsigned long pos_byte_end = pos_byte_beg + n_bytes
    for i in range(number_of_records):
            buf[i] = bytes(bit_stream[pos_byte_beg + record_byte_size * i:\
                    pos_byte_end + record_byte_size * i])
    return buf

cdef inline read_array(const char* bit_stream, str record_format, unsigned long long number_of_records,
        unsigned long record_byte_size, unsigned long pos_byte_beg, unsigned long n_bytes,
        unsigned long bit_count, unsigned char bit_offset, unsigned char swap):
    cdef np.ndarray buf = np.empty(number_of_records, dtype=record_format)  # return numpy array
    cdef unsigned long long i
    cdef unsigned long pos_byte_end = pos_byte_beg + n_bytes
    for i in range(number_of_records):
        buf[i] = np.fromstring(bit_stream[pos_byte_beg + record_byte_size * i:\
            pos_byte_end + record_byte_size * i], dtype=record_format)
    if swap == 0:
        return buf
    else:
        return buf.byteswap()

def unsorted_data_read4(record, info, bytes tmp,
                        const unsigned short record_id_size,
                        const unsigned long long data_block_length):
    """ reads only the channels using offset functions, channel by channel within unsorted data

    Parameters
    ------------
    record : class
        record class
    info: class
        info class
    tmp : bytes
        byte stream
    record_id_size : unsigned short
        record id length
    data_block_length : unsigned long long
        length of data block minus header

    Returns
    --------
    buf : array
        data array

    """
    cdef const char* bit_stream = PyBytes_AsString(tmp)
    cdef unsigned long long position = 0
    cdef unsigned char record_id_char = 0
    cdef unsigned short record_id_short = 0
    cdef unsigned long record_id_long = 0
    cdef unsigned long long record_id_long_long = 0
    # initialise data structure
    # key is channel name
    cdef dict buf = {}
    cdef dict VLSD = {}
    cdef dict pos_byte_beg = {}
    cdef dict pos_byte_end = {}
    cdef dict c_format_structure = {}
    cdef dict byte_length = {}
    cdef dict numpy_format = {}
    # key is record id
    cdef dict index = {}
    cdef dict CGrecordLength = {}
    cdef dict VLSD_flag = {}
    cdef dict VLSD_CG_name = {}
    cdef dict VLSD_CG_signal_data_type = {}
    cdef dict channel_name_set = {}
    for record_id in record:
        if record[record_id]['record'].Flags & 0b1:
            VLSD_flag[record_id] = True
            VLSD[record[record_id]['record'].VLSD_CG[record_id]['channelName']] = []
            VLSD_CG_name[record_id] = record[record_id]['record'].VLSD_CG[record_id]['channelName']
            VLSD_CG_signal_data_type[record_id] = record[record_id]['record'].VLSD_CG[record_id]['channel'].signal_data_type(info)
        else:
            VLSD_flag[record_id] = False
            for Channel in record[record_id]['record'].values():
                #if not Channel.VLSD_CG_Flag:
                buf[Channel.name] = np.empty((record[record_id]['record'].numberOfRecords,),
                                             dtype='V{}'.format(Channel.nBytes_aligned), order ='C')
                numpy_format[Channel.name] = Channel.data_format(info)
                pos_byte_beg[Channel.name] = record_id_size + Channel.byteOffset
                pos_byte_end[Channel.name] = pos_byte_beg[Channel.name] + Channel.nBytes_aligned
            index[record_id] = 0
            CGrecordLength[record_id] = record[record_id]['record'].CGrecordLength
            channel_name_set[record_id] = record[record_id]['record'].channelNames
    # read data
    if record_id_size == 1:
        while position < data_block_length:
            memcpy(&record_id_char, &bit_stream[position], 1)
            position, buf, VLSD, index = unsorted_read4(bit_stream, tmp, record_id_char, 1,
                                                        position, buf, VLSD, pos_byte_beg, pos_byte_end,
                                                        c_format_structure, index, CGrecordLength,
                                                        VLSD_flag, VLSD_CG_name, VLSD_CG_signal_data_type, channel_name_set)
    elif record_id_size == 2:
        while position < data_block_length:
            memcpy(&record_id_short, &bit_stream[position], 2)
            position, buf, VLSD, index = unsorted_read4(bit_stream, tmp, record_id_short, 2,
                                                        position, buf, VLSD, pos_byte_beg, pos_byte_end,
                                                        c_format_structure, index, CGrecordLength,
                                                        VLSD_flag, VLSD_CG_name, VLSD_CG_signal_data_type, channel_name_set)
    elif record_id_size == 3:
        while position < data_block_length:
            memcpy(&record_id_long, &bit_stream[position], 4)
            position, buf, VLSD, index = unsorted_read4(bit_stream, tmp, record_id_long, 4,
                                                        position, buf, VLSD, pos_byte_beg, pos_byte_end,
                                                        c_format_structure, index, CGrecordLength,
                                                        VLSD_flag, VLSD_CG_name, VLSD_CG_signal_data_type, channel_name_set)
    elif record_id_size == 4:
        while position < data_block_length:
            memcpy(&record_id_long_long, &bit_stream[position], 8)
            position, buf, VLSD, index = unsorted_read4(bit_stream, tmp, record_id_long_long, 8,
                                                        position, buf, VLSD, pos_byte_beg, pos_byte_end,
                                                        c_format_structure, index, CGrecordLength,
                                                        VLSD_flag, VLSD_CG_name, VLSD_CG_signal_data_type, channel_name_set)
    # changing from bytes type to desired type
    if buf:
        for name in buf.keys():
            buf[name] = buf[name].view(dtype=numpy_format[name])
    # convert list to array for VLSD only
    if VLSD:
        for channel_name in VLSD:
            VLSD[channel_name] = np.array(VLSD[channel_name])
        buf.update(VLSD)
    return buf

cdef inline unsorted_read4(const char* bit_stream, bytes tmp, record_id,
                           unsigned short record_id_size, unsigned long long position,
                           buf, VLSD, pos_byte_beg, pos_byte_end, c_format_structure,
                           index, CGrecordLength, VLSD_flag, VLSD_CG_name, VLSD_CG_signal_data_type,
                           channel_name_set):
    cdef unsigned long VLSDLen = 0
    if not VLSD_flag[record_id]:  # not VLSD CG)
        for channel_name in channel_name_set[record_id]:  # list of channel classes
            buf[channel_name][index[record_id]] = \
                   tmp[position + pos_byte_beg[channel_name]:position + pos_byte_end[channel_name]]
        index[record_id] += 1
        position += CGrecordLength[record_id]
    else:  # VLSD CG
        position += <unsigned long long> record_id_size
        memcpy(&VLSDLen, &bit_stream[position], 4)  # VLSD length
        position += 4
        signal_data_type = VLSD_CG_signal_data_type[record_id]
        if signal_data_type == 6:
            temp = bit_stream[position:position + VLSDLen - 1].decode('ISO8859')
        elif signal_data_type == 7:
            temp = bit_stream[position:position + VLSDLen - 1].decode('utf-8')
        elif signal_data_type == 8:
            temp = bit_stream[position:position + VLSDLen - 1].decode('<utf-16')
        elif signal_data_type == 9:
            temp = bit_stream[position:position + VLSDLen - 1].decode('>utf-16')
        VLSD[VLSD_CG_name[record_id]].append(temp)
        position += <unsigned long long> VLSDLen
    return position, buf, VLSD, index


def sd_data_read(unsigned short signal_data_type, bytes sd_block,
                 unsigned long long sd_block_length, unsigned long long n_records):
    """ Reads vlsd channel from its SD Block bytes

    Parameters
    ----------------
    signal_data_type : int

    sd_block : bytes
        SD Block bytes

    sd_block_length: int
        SD Block data length (header not included)

    n_records: int
        number of records

    Returns
    -----------
    array
    """
    cdef const char* bit_stream = PyBytes_AsString(sd_block)
    cdef unsigned long max_len = 0
    cdef unsigned long vlsd_len = 0
    cdef unsigned long *VLSDLen = <unsigned long *> PyMem_Malloc(n_records * sizeof(unsigned long))
    cdef unsigned long long *pointer = <unsigned long long *> PyMem_Malloc(n_records * sizeof(unsigned long long))
    cdef unsigned long long rec = 0
    if not VLSDLen or not pointer:
        raise MemoryError()
    try:
        pointer[0] = 0
        VLSDLen[0] = 0
        for rec from 0 <= rec < n_records - 1 by 1:
            memcpy(&vlsd_len, &bit_stream[pointer[rec]], 4)
            VLSDLen[rec] = vlsd_len
            pointer[rec + 1] = VLSDLen[rec] + 4 + pointer[rec]
            if VLSDLen[rec] > max_len:
                    max_len = VLSDLen[rec]
        memcpy(&vlsd_len, &bit_stream[pointer[rec]], 4)
        VLSDLen[rec] = vlsd_len
        if VLSDLen[rec] > max_len:
            max_len = VLSDLen[rec]
        if max_len != 0:
            if signal_data_type < 10:
                if signal_data_type == 6:
                    channel_format = 'ISO8859'
                elif signal_data_type == 7:
                    channel_format = 'utf-8'
                elif signal_data_type == 8:
                    channel_format = '<utf-16'
                elif signal_data_type == 9:
                    channel_format = '>utf-16'
                else:
                    channel_format = 'utf-8'
                    printf('signal_data_type should have fixed length')
                return equalize_string_length(bit_stream, pointer, VLSDLen, max_len, n_records, channel_format)
            else:  # byte arrays or mime types
                return equalize_byte_length(bit_stream, pointer, VLSDLen, max_len, n_records)
        else:
            printf('VLSD channel could not be properly read\n')
            return None
    finally:
        PyMem_Free(pointer)
        PyMem_Free(VLSDLen)

cdef inline equalize_byte_length(const char* bit_stream, unsigned long long *pointer, unsigned long *VLSDLen,
                                 unsigned long max_len, unsigned long long n_records):
    cdef np.ndarray output = np.zeros((n_records, ), dtype='V{}'.format(max_len))
    cdef unsigned long rec = 0
    for rec from 0 <= rec < n_records by 1:  # resize string to same length, numpy constrain
        output[rec] = bytearray(bit_stream[pointer[rec]+4:pointer[rec]+4+VLSDLen[rec]]).rjust(max_len,  b'\x00')
    return output

cdef inline equalize_string_length(const char* bit_stream, unsigned long long *pointer, unsigned long *VLSDLen,
                                   unsigned long max_len, unsigned long long n_records, channel_format):
    cdef np.ndarray output = np.zeros((n_records, ), dtype='U{}'.format(max_len))
    cdef unsigned long rec = 0
    for rec from 0 <= rec < n_records by 1:  # resize string to same length, numpy constrain
        output[rec] = bit_stream[pointer[rec]+4:pointer[rec]+4+VLSDLen[rec]].decode(channel_format).rstrip('\x00')
    return output