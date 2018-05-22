# coding=utf-8
from typing import List, Dict, Tuple

__algorithm__ = 'GZIP'
__group__ = "LZ"


def lcp(text: str, start: int, initial: List[int]) -> (int, int):
    common = text[start:]
    index = [3] * len(initial)
    stop = [0] * len(initial)

    for i, pos in enumerate([x for x in initial]):
        for j in range(3, len(common)):
            if stop[i]:
                continue
            if text[pos + j] == common[j]:
                index[i] += 1
            else:
                stop[i] = 1

    lcp_size = max(index)
    return initial[index.index(lcp_size)], lcp_size


def encode(text: str, window: int = 0) -> Dict:
    """
    >>> encode('mississippi')
    {'pairs': [(0, 'm'), (0, 'i'), (0, 's'), (0, 's'), (3, 4), (0, 'p'), (0, 'p'), (0, 'i')], 'encoded': 'm i s s 4,3 p p i'}

    :param text:
    :param window:
    :return:
    """
    encoded = []
    table = {}

    p = 0
    size = len(text)

    while True:

        gram = text[p:p + 3]

        if window and gram in table:

            ls = list(filter(lambda x: x >= p - window, table[gram]))

            if not ls:
                del table[gram]
            else:
                table[gram] = ls

        if gram not in table:
            table[gram] = [p]
            encoded.append((0, gram[0]))
            p += 1
        else:
            i, common = lcp(text, p, table[gram])
            encoded.append((p - i, common))
            table[gram].append(p)
            p += common

        if p == size:
            break

    return {'pairs': encoded}


def decode(encoded: List[Tuple[int, str]]) -> str:
    """
    >>> decode([(0, 'm'), (0, 'i'), (0, 's'), (0, 's'), (3, 4), (0, 'p'), (0, 'p'), (0, 'i')])
    'mississippi'

    :param encoded:
    :return:
    """
    decoded = ""
    size = 0

    for a, b in encoded:
        if a:
            b = int(b)
            start = size - a
            end = start + b
            tmp = decoded[start: end]
            repeat = b - a
            if repeat:
                tmp += tmp[:repeat]
            decoded += tmp
            size += b
        else:
            decoded += b
            size += 1

    return decoded


if __name__ == '__main__':
    encode_result = encode('mississippi')
    decode_result = decode(encode_result['pairs'])
