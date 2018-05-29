# coding=utf-8
from typing import List, Dict, Tuple

from .utils import input_example

__algorithm__ = 'GZIP'
__group__ = "LZ"
__author__ = 'Francesco Saverio Cannizzaro'


def lcp(text: str, start: int, initial: List[int]) -> (int, int):
    common = text[start:]
    index = [3] * len(initial)
    stop = [0] * len(initial)

    print(start, initial, common)

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


def update(last_remove: int, start: int, l: int, text: str, table: Dict) -> int:
    to_insert = [(text[i:i + 3], i) for i in range(start, l)]
    to_remove = [text[i:i + 3] for i in range(last_remove, last_remove + l)]

    for gram in to_remove:
        if gram in table:
            table[gram] = table[gram][1:]
            if not len(table[gram]):
                del table[gram]

    for gram, i in to_insert:
        if gram in table:
            table[gram].append(i)
        else:
            table[gram] = [i]

    return last_remove + l

def ensure_list(table, key):
    if key not in table:
        table[key] = []
    return table[key]    

@input_example(text='mississippi')
def encode(text: str) -> Dict:
    """
    >>> encode('mississippi')
    {'pairs': [(0, 'm'), (0, 'i'), (0, 's'), (0, 's'), (3, 4), (0, 'p'), (0, 'p'), (0, 'i')], 'encoded': 'm i s s 4,3 p p i'}

    :param text:
    :return:
    """

    last_remove = 0
    encoded = []
    table = {}

    p = 0
    size = len(text)

    while True:

        gram = text[p:p + 3]

        if gram not in table:
            table[gram] = [p]
            encoded.append((0, gram[0]))
            p += 1
        else:
            i, common = lcp(text, p, table[gram])
            encoded.append((p - i, common))
            last_remove = update(last_remove, p - i, p, text, table)
            ensure_list(table, gram).append(p)
            p += common

        if p == size:
            break

    return {'pairs': encoded}


@input_example(text='---')
def decode(encoded: List[Tuple[int, str]]) -> str:
    """
    >>> decode([(0, 'm'), (0, 'i'), (0, 's'), (0, 's'), (3, 4), (0, 'p'), (0, 'p'), (0, 'i')])
    'mississippi'

    :param encoded:
    :return:
    """
    decoded = ''
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
    with open('./divina_commedia.txt') as file:
        content = file.read()
        encode_result = encode(content)
        # decode_result = decode(encode_result['pairs'])
        print(encode_result)
        # print(decode_result)
