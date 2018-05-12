# coding=utf-8
from typing import List, Tuple, Dict

from .utils import timer

__algorithm__ = "LZ78"
__group__ = "LZ"


def encode(text: str) -> Dict[str, List[Tuple[int, str]]]:
    """
    >>> encode('ccaccbcabcaba')
    [(0, 'c'), (1, 'a'), (1, 'c'), (0, 'b'), (2, 'b'), (5, 'a')]
    """
    codebook = dict()
    codebook[''] = 0
    i = 0
    count = 1
    output = list()
    N = len(text)
    while i < N:
        ii = i
        while ii < N:
            pattern = text[i:(ii + 1)]
            if pattern in codebook:
                ii += 1
            else:
                break
        codebook[pattern] = count
        output.append((codebook[pattern[:-1]], text[ii] if ii < N else text[ii - 1]))
        count += 1
        i += len(pattern)
    return {'pairs': output}


def decode(list_: List[Tuple[int, str]]) -> str:
    """
    >>> decode([(0, 'c'), (1, 'a'), (1, 'c'), (0, 'b'), (2, 'b'), (5, 'a')])
    'ccaccbcabcaba'
    """
    codebook = dict()
    codebook[0] = ''
    s = ''
    for t in list_:
        tmp = codebook[t[0]] + t[1]
        codebook[len(codebook)] = tmp
        s += tmp
    return s


def main():
    lines = 'ccaccbcabcaba'
    with timer('encoding lz78'):
        encoded = encode(lines)
        # print(encoded)
    with timer('decoding lz78'):
        decoded = decode(encoded)
        # print(decoded)
    assert lines == decoded


if __name__ == '__main__':
    main()
