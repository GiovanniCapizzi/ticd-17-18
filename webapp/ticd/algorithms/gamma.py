# coding=utf-8
from collections import deque  # https://docs.python.org/2/library/collections.html#collections.deque
from math import log
from typing import List

__algorithm__ = 'Gamma'
__group__ = "integers"


def encode(input_integers_list: List[int]) -> str:
    """
    >>> encode([12, 12])
    '00011000001100'
    >>> assert decode(encode(list(range(1, 1000)))) == list(range(1, 1000))
    """
    return "".join(['0' * int(log(n, 2)) + "{0:b}".format(n) for n in input_integers_list])


def decode(input_binary_string: str) -> List[int]:
    """
    >>> decode('00011000001100')
    [12, 12]
    """
    queue = deque(input_binary_string)
    output = []
    N = 0
    while len(queue):
        bit = queue.popleft()
        if bit is '0':
            N += 1
        else:
            temp = '1'
            while N:
                temp += queue.popleft()
                N -= 1
            output.append(int(temp, 2))
    return output


if __name__ == '__main__':
    pass
