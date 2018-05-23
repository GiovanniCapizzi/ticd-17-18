# coding=utf-8
from collections import deque

from .suffix_array import calculate as suffix_array
from .utils import input_example

__algorithm__ = 'BWT'
__group__ = "miscellaneous"


@input_example(text='mississippi')
def encode(text: str, use_suffix_array: bool = False) -> str:
    """
    >>> encode('mississippi', True)
    'ipssm$pissii'

    :param text:
    :param use_suffix_array:
    :return:
    """
    text += '$'

    if use_suffix_array:
        sa = suffix_array(text)
        return ''.join([text[sa[i] - 1] if sa[i] > 0 else text[-1] for i in range(len(text))])

    rotations = []
    start = deque(text)

    for _ in range(len(text)):
        start.rotate(1)
        rotations.append(''.join(start))

    return ''.join(map(lambda rot: rot[-1], sorted(rotations)))


@input_example(encoded='ipssm$pissii')
def decode(encoded: str) -> str:
    """
    >>> decode('ipssm$pissii')
    'mississippi'

    :param encoded:
    :return:
    """
    t = encoded.index('$')
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
