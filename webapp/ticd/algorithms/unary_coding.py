# coding=utf-8
from typing import List

__algorithm__ = "Unary"
__group__ = "integers"


def encode_unary(list_of_integers: List[int]) -> str:
    """
    >>> encode_unary([13, 13])
    '00000000000010000000000001'
    >>> assert [decode_unary(encode_unary([i]))[0] for i in range(1, 100)] == [i for i in range(1, 100)]
    """

    return "".join(["0" * (n - 1) + "1" for n in list_of_integers])


def decode_unary(binary_string: str) -> List[int]:
    """
    >>> decode_unary('00000000000010000000000001')
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
    return result
