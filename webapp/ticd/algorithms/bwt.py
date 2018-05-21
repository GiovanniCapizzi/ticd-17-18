# coding=utf-8
from collections import deque
from typing import Dict

from .suffix_array import sa as suffix_array

__algorithm__ = 'BWT'
__group__ = "miscellaneous"


def encode(text: str, use_suffix_array: bool = False) -> Dict:
    """
    >>> encode('mississippi', True)
    'ipssmhpissii'

    :param text:
    :param use_suffix_array:
    :return:
    """
    text += chr(ord(min(text)) - 1)

    def ret(encoded):
        return {
            'encoded': encoded,
            'EOS': text[-1]
        }

    if use_suffix_array:
        sa = suffix_array(text)
        return ret(''.join([text[sa[i] - 1] if sa[i] > 0 else text[-1] for i in range(len(text))]))

    rotations = []
    start = deque(text)

    for _ in range(len(text)):
        start.rotate(1)
        rotations.append(''.join(start))

    return ret(''.join(map(lambda rot: rot[-1], sorted(rotations))))


def decode(encoded: str) -> str:
    """
    >>> decode('ipssmhpissii')
    'mississippi'

    :param encoded:
    :return:
    """
    t = encoded.index(min(encoded))
    pre = sorted(enumerate(encoded), key=lambda v: v[1])
    f = ''.join(c for p, c in pre)
    tao = [p for p, c in pre]
    w = f[t]
    for _ in range(1, len(encoded)):
        t = tao[t]
        w += f[t]
    return w[:-1]


if __name__ == '__main__':
    to_encode = 'mississippi'
    encoded_sa = encode(to_encode, True)
    encoded_basic = encode(to_encode)
    print(' >> encoding', to_encode, 'to [suffix-array]', encoded_sa, '[basic]', encoded_basic)
    decoded = decode(encoded_sa)
    print(' >> decoding', encoded_sa, 'to ', decoded)
