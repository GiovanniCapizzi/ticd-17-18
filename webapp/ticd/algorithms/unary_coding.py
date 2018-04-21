# coding=utf-8
from typing import List


def unary_coding(n: int) -> str:
    """
    >>> unary_coding(13)
    '0000000000001'
    >>> assert [unary_decoding(unary_coding(i))[0] for i in range(1, 100)] == [i for i in range(1, 100)]
    """
    return "0" * (n - 1) + "1"


def unary_decoding(s: str) -> List[int]:
    """
    >>> unary_decoding('00000000000010000000000001')
    [13, 13]
    """
    as_list = list(s)
    result = []
    while len(as_list) != 0:
        zeros = 0
        while as_list[0] == '0':
            as_list.pop(0)
            zeros += 1
        as_list.pop(0)
        result.append(zeros + 1)
    return result
