# coding=utf-8
from typing import List

from .utils import input_example, integers_decode, integers_encode

__algorithm__ = "Unary"
__group__ = "integers"
__author__ = "Mirko Avantaggiato"


@input_example(list_of_integers="46 33 13 1 48 23 34 13 15 3")
def encode_unary(list_of_integers: List[int]) -> str:
    """
    >>> encode_unary([13, 13])
    '0000000000000000000000000100000000000000000000000001'
    >>> assert [decode_unary(encode_unary([i]))[0] for i in range(1, 100)] == [i for i in range(1, 100)]
    """
    list_of_integers = integers_encode(list_of_integers)
    if 0 in list_of_integers:
        return 'Cannot encode.'

    return "".join(["0" * (n - 1) + "1" for n in list_of_integers])


@input_example(
        binary_string="0000000000000000000000000100000000000000000000000001")
def decode_unary(binary_string: str) -> List[int]:
    """
    >>> decode_unary('0000000000000000000000000100000000000000000000000001')
    [13, 13]
    """
    as_list = list(binary_string)
    result = []
    while len(as_list) != 0:
        zeros = 0
        while as_list[0] == '0':
            as_list.pop(0)
            zeros += 1
        as_list.pop(0)
        result.append(zeros + 1)
    return integers_decode(result)
