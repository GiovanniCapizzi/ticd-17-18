# coding=utf-8
from collections import deque
from functools import reduce

from .suffix_array import KS


def encode(text, use_suffix_array=False):
    """
    >>> encode('mississippi', True)
    ('ipssmhpissii', 'h')

    :param text:
    :param use_suffix_array:
    :return:
    """
    text += chr(ord(min(text)) - 1)

    if use_suffix_array:
        try:
            sa = KS(text)
        except OSError:
            from .suffix_array import suffix_array
            sa = suffix_array(text)
        return ''.join([text[sa[i] - 1] if sa[i] > 0 else text[-1] for i in range(len(text))]), text[-1]

    rotations = []
    start = deque(text)

    for _ in range(len(text)):
        start.rotate(1)
        rotations.append(''.join(start))

    return ''.join(map(lambda rot: rot[-1], sorted(rotations))), text[-1]


def decode(l):
    """
    >>> decode('ipssmhpissii')
    'mississippi'

    :param l:
    :return:
    """
    t = l.index(min(l))
    f = sorted(l)
    w = f[t]
    tao = {char: [] for char in set(f)}
    for pos, char in enumerate(l):
        tao[char].append(pos)
    tao = reduce(list.__add__, map(lambda x: x[1], sorted(tao.items())))
    for _ in range(1, len(l)):
        t = tao[t]
        w += f[t]
    return w[:-1]


if __name__ == '__main__':
    to_encode = 'mississippi'
    encoded_sa, eos = encode(to_encode, True)
    encoded_basic, _ = encode(to_encode)
    print(' >> encoding', to_encode, 'to [suffix-array]', encoded_sa, '[basic]', encoded_basic, ', $ =', eos)
    decoded = decode(encoded_sa)
    print(' >> decoding', encoded_sa, 'to ', decoded)
