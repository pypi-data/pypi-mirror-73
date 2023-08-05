# -*- coding: utf-8 -*-
# @author: leesoar

import copy
import ctypes

__all__ = ["partition", "b64encode", "b64decode", "shift_overflow", "left_shift", "unsigned_right_shift"]

_base64_map = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
_base58_map = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def partition(array, size):
    """Equal parts array

    Args:
        array: pending array
        size: list size after split
    """
    array_is_str = False
    if type(array) == str:
        array_is_str = True
        tmp_array = list(array)
    else:
        tmp_array = copy.deepcopy(array)

    for i in range(0, len(tmp_array), size):
        if array_is_str:
            yield ''.join(tmp_array[i: i + size])
        else:
            yield tmp_array[i: i + size]


def b64encode(byte_str: bytes or bytearray, b64_map=_base64_map) -> str:
    """Base64 encode

    Support custom mapping.

    Args:
        byte_str: byte string
        b64_map: default base64 mapping
    Returns:
        string for base64
    """
    assert isinstance(byte_str, (bytes, bytearray)), \
        r"byte_str's type must be bytes or bytearray"

    bit_str = ''.join(map(lambda x: bin(x).lstrip("0b").zfill(8), byte_str))
    bit_str += (6 - (len(bit_str) % 6 or 6)) * "0"
    pos = [int(x, base=2) for x in partition(bit_str, size=6)]
    return ''.join([b64_map[i] for i in pos]) + "=" * (3 - (len(byte_str) % 3 or 3))


def b64decode(b64_str: str, b64_map=_base64_map) -> bytes:
    """Base64 decode

    Support custom mapping.

    Args:
        b64_str: base64 string
        b64_map: default base64 mapping
    Returns:
        byte string
    """
    assert isinstance(b64_str, str), \
        r"b64_str's type must be str"

    nil_count = b64_str.count("=")
    filled_zero_count = (len(b64_str) - nil_count) * 6 % 8
    bit_str = "".join(map(lambda x: bin(x).lstrip("0b").zfill(6),
                          (map(b64_map.find, b64_str[:-nil_count or None]))))[:-filled_zero_count or None]
    return bytes([int(x, base=2) for x in partition(bit_str, size=8)])


def shift_overflow(n: int, base=32) -> int:
    """shift overflow

    Python's int is infinite length.

    It will turn to long.

    So this function will overflow it.

    The default is int32.

    Args:
        n: shifted value
        base: int's bit length. the default is 32 means int32
    Return:
        overflowed value
    """
    signed_int = 2 ** (base-1)
    max_int = signed_int - 1
    min_int = -signed_int

    if min_int <= n <= max_int:
        return n
    return (n + signed_int) % (2 * signed_int) - signed_int


def left_shift(n: int, i: int) -> int:
    """overflow left shift

    like JavaScript '<<'

    Args:
        n: int value
        i: shift amount
    Return:
        shifted value
    """
    return shift_overflow(n << i)


def unsigned_right_shift(n: int, i: int) -> int:
    """unsigned right shift

    like JavaScript '>>>'

    Args:
        n: int value
        i: shift amount
    Return:
        shifted value
    """
    if n < 0:
        n = ctypes.c_uint32(n).value

    return shift_overflow(n >> i)


def dec_to_other(digit: int, base=58, array: list = None) -> list:
    """Decimal to other

    Convert from decimal to other base

    Args:
        digit: decimal number
        base: just base, like 64, 128, 2, etc.
        array: no need for attention, just the return value
    Return:
        other base array
    """
    array = array or []
    quotient, mod = divmod(digit, base)
    array.append(mod)
    if quotient >= base:
        return dec_to_other(quotient, base, array)
    array.append(quotient)
    return array[::-1]


def b58encode(s: str, b58_map=_base58_map) -> str:
    """Base58 encode

    Support custom mapping.

    Args:
        s: string
        b58_map: default base58 mapping
    Returns:
        string for base58
    """
    dec_sum = sum(map(lambda x: x[1] * 256 ** x[0], enumerate(bytes(s.encode())[::-1])))
    b58_array = dec_to_other(dec_sum)
    return "".join(map(lambda x: b58_map[x], b58_array))


def b58decode(b58_str: str, b58_map=_base58_map) -> str:
    """Base58 decode

    Support custom mapping.

    Args:
        b58_str: base58 string
        b58_map: default base58 mapping
    Returns:
        string
    """
    b58_array = list(map(lambda x: b58_map.find(x), b58_str))
    dec_sum = sum(map(lambda x: x[1] * 58 ** x[0], enumerate(b58_array[::-1])))
    return bytes(dec_to_other(dec_sum, base=256)).decode()
