import time
from typing import List, Tuple
from .utils import timer

def encode(s: str) -> List[Tuple[int, str]]:
    """
    >>> encode('ccaccbcabcaba')
    [(0, 'c'), (1, 'a'), (1, 'c'), (0, 'b'), (2, 'b'), (5, 'a')]
    """
    codebook = dict()
    codebook[''] = 0
    i = 0
    count = 1
    output = list()
    N = len(s)
    while i < N:
        ii = i
        while ii < N:
            pattern = s[i:(ii + 1)]
            if pattern in codebook:
                ii += 1
            else:
                break
        codebook[pattern] = count
        output.append((codebook[pattern[:-1]], s[ii] if ii < N else s[ii - 1]))
        count += 1
        i += len(pattern)
    return output


def decode(list_: list) -> str:
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
        #print(encoded)
    with timer('decoding lz78'):
        decoded = decode(encoded)
        #print(decoded)
    assert lines == decoded


if __name__ == '__main__':
    main()
