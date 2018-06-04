# coding=utf-8
from typing import Dict, List

from .utils import integers_decode, integers_encode, input_example

__algorithm__ = "Levenshtein"
__author__ = "Francesco Landolina"
__group__ = "integers"


@input_example(integers_list="1, 0, 2, 10231, 11")
def encode(integers_list: List[int]) -> Dict[str, str]:
    """
    >>> encode([1, 0, 2, 10231, 11])['bit_string']
    '11000111000011110111000111111101110111100000110'
    """
    output = ''
    integers_list = integers_encode(integers_list)
    for x in integers_list:
        if x == 0:
            output += '0'
        else:
            C = 1
            b_n = '{0:b}'.format(x)
            tmp = b_n[1:]
            M = tmp
            while len(M) != 0:
                M = '{0:b}'.format(len(M))[1:]
                tmp = M + tmp
                C += 1
            result = ('1' * C) + '0' + tmp
            output += result
    return {"bit_string": output}


@input_example(bit_string="11000111000011110111000111111101110111100000110")
def decode(bit_string: str) -> List[int]:
    """
    >>> decode('11000111000011110111000111111101110111100000110')
    [1, 0, 2, 10231, 11]
    """
    in_list = list(bit_string)
    # print(in_list)
    results = list()
    s = None
    while len(in_list) != 0:
        N = 0
        while in_list[0] == '1':
            in_list.pop(0)
            N += 1
        in_list.pop(0)
        if N == 0:
            results.append(0)
        elif N == 1:
            results.append(1)
        else:
            t = 1
            for _ in range(N - 1):
                # print('t :' + str(t))
                s = '1'
                for _ in range(t):
                    s += in_list.pop(0)
                t = int(s, 2)
            results.append(int(s, 2))

    return integers_decode(results)


def main():
    print('-----Levenshtein-----')
    print('encode')
    bits = encode([1, 0, 2, 10231, 11])
    print(bits)
    print('decode')
    integers = decode(bits["bit_string"])
    print(integers)


if __name__ == '__main__':
    main()
