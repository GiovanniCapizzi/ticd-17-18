# coding=utf-8
from typing import List

from bitstring import BitArray


def encode(x: int)-> str:
    """
    >>> encode(10231)
    '1111011010011111110111'
    """
    if x == 0:
        return str(BitArray(bin='0').bin)
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
        return str(BitArray(bin=result).bin)


def decode(b: str) -> List[int]:
    """
    >>> decode('11110000000011110000000011100111110011')
    [16, 16, 7, 7]
    """
    in_list = list(b)
    # print(in_list)
    results = list()
    while len(in_list) != 0:
        N = 0
        while in_list[0] == '1':
            in_list.pop(0)
            N += 1
        if N == 0:
            results.append(0)
        else:
            # print('N :' + str(N))
            in_list.pop(0)
            # print(N)
            t = 1
            for _ in range(N - 1):
                # print('t :' + str(t))
                s = '1'
                for _ in range(t):
                    s += in_list.pop(0)
                t = int(s, 2)
            results.append(int(s, 2))

    return results


def main():
    print('-----Levenshtein-----')
    print('encode')
    bits = encode(10231)
    print(bits)
    print('decode')
    integers = decode('11110000000011110000000011100111110011')
    print(integers)


if __name__ == '__main__':
    main()
