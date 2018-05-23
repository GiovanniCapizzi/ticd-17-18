# coding=utf-8


from .utils import input_example

from typing import List

sequences = [0, 1]

__algorithm__ = 'Fibonacci'
__group__ = 'integers'


def fibonacci(value):
    if sequences[-1] < value:
        sequences.append(sequences[-1] + sequences[-2])
    return sequences


@input_example(integers="5 5 5 8 13")
def encode(integers: List[int]) -> str:
    """
    >>> encode([5, 5, 5, 8, 13])
    '0001100011000110000110000011'

    :param integers:
    :return:
    """
    symbols = {}

    for integer in set(integers):
        tmp = integer
        fns = []

        while tmp > 0:
            value = max(filter(lambda x: x <= tmp, fibonacci(tmp)))
            fns.append(max(0, sequences.index(value) - 2))
            tmp -= value

        symbols[integer] = ''.join(['1' if x in fns else '0' for x in range(max(fns) + 1)]) + '1'

    return ''.join([symbols[integer] for integer in integers])


@input_example(encoded="0001100011000110000110000011")
def decode(encoded: str) -> List[int]:
    """
    >>> decode('0001100011000110000110000011')
    [5, 5, 5, 8, 13]

    :param encoded:
    :return:
    """

    if encoded == '11':
        return [1]
    integers = map(lambda x: x + '1', filter(lambda x: x, encoded.split('11')))
    return [sum([sequences[x + 2] for x, value in enumerate(integer) if value == '1']) for integer in integers]


if __name__ == '__main__':
    import time

    start_time = time.clock()
    to_encode = [5, 5, 5, 8, 13]
    enc = encode(to_encode)
    print(" >> encoding", to_encode, " to ", enc)
    decoded = decode(enc)
    print(" >> decoding", enc, 'to', decoded)
    print("execution time", time.clock() - start_time, "seconds")
