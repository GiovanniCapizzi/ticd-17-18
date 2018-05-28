# coding=utf-8
from typing import Dict, List

from mpmath import mp, mpf

from .utils import input_example

mp.prec = 1000000

# increase value up to very high values to increase precision


__algorithm__ = "Arithmetic Coding"
__group__ = "miscellaneous"
__author__ = "Francesco Landolina"


class Range(object):
    def __init__(self, low: mpf, high: mpf):
        self.low = low
        self.high = high

    def __contains__(self, item: float):
        return self.low <= item < self.high

    def __str__(self):
        return "[{}, {})".format(self.low, self.high)

    def __repr__(self):
        return self.__str__()

    def get_low(self):
        return self.low

    def get_high(self):
        return self.high

    def set_low(self, low: float):
        self.low = low

    def ampiezza(self):
        return self.high - self.low


def source_prob(s: str):
    _dict = dict()
    for c in s:
        if c not in _dict:
            _dict[c] = 0
        _dict[c] += 1 / len(s)
    sorted(_dict)
    return _dict


@input_example(text="abbabaaaa", precision="10000")
def encode(text: str, precision: int = 100, is_static: bool = True) -> Dict:
    mp.prec = precision
    if is_static:
        real, codebook = enc_static(text)
        out = dec_static(real, codebook)
    else:
        real, codebook = enc_dynamic(text)
        out = dec_dynamic(real, codebook)
    return {'encoded': str(real), 'codebook': codebook, 'decoded': str(out)}


def enc_dynamic(input_text: str) -> (mpf, List[str]):
    """
    >>> enc_dynamic('aaaabaaaa')
    (mpf('0.5263107263107262766304979'), ['$', 'a', 'b'])
    """
    s = input_text
    s += '$'
    current_range = Range(mpf(0), mpf(1))
    A = sorted(set(s))
    dict_prob = dict()
    for e in A:
        dict_prob[e] = 1
    num_ele = len(A)

    for c in s:
        new_ranges = split_interval(current_range,
                                    zip(dict_prob.keys(), list(map(lambda x: x / num_ele, dict_prob.values()))))
        current_range = new_ranges[c]
        dict_prob[c] += 1
        num_ele += 1
    return current_range.get_low(), A


def dec_dynamic(input_number: mpf, set_of_symblols: list) -> str:
    """
    >>> dec_dynamic(mpf('0.5263107263107262766304979'), ['$', 'a', 'b'])
    'aaaabaaaa'
    """
    enc = input_number
    current_range = Range(mpf(0), mpf(1))
    A = sorted(set_of_symblols)
    dict_prob = dict()
    for e in A:
        dict_prob[e] = 1
    num_ele = len(A)
    s = ''
    while True:
        new_ranges = split_interval(current_range,
                                    zip(dict_prob.keys(), list(map(lambda x: x / num_ele, dict_prob.values()))))
        for c in new_ranges.keys():
            # print(' {}  {} {}'.format(enc, new_ranges[c], enc in new_ranges[c]))
            if enc in new_ranges[c]:
                current_range = new_ranges[c]
                s += c
                dict_prob[c] += 1
                num_ele += 1
                # print(str(c) + str(new_ranges))
                break
        if current_range.get_low() == enc:
            break
    if s[-1] == '$':
        s = s[:-1]
    return s


def enc_static(s: str) -> (str, Dict[str, float]):
    """
    >>> enc_static('aaaabaaaa')
    (mpf('0.67593139199999975394545314'), {'a': 0.7999999999999999, 'b': 0.1, '$': 0.1})
    """
    s += '$'
    source = source_prob(s)
    current_range = Range(mpf(0), mpf(1))
    tmp = sorted(zip(source.keys(), source.values()))
    ranges = bound(tmp)
    for c in s:
        current_range = new_range(current_range, ranges[c])
    return current_range.get_low(), source


def dec_static(input_number: mpf, source: Dict[str, float]) -> str:
    """
    >>> dec_static(mpf('0.67593139199999975394545314'), {'a': 0.7999999999999999, 'b': 0.1, '$': 0.1})
    'aaaabaaaa'
    """
    enc = input_number
    current_range = Range(mpf(0), mpf(1))
    tmp = sorted(zip(source.keys(), source.values()))
    ranges = bound(tmp)
    s = ''
    while True:
        for c in ranges.keys():
            # print(' {}  {} {}'.format(enc, new_ranges[c], enc in new_ranges[c]))
            tmp_range = new_range(current_range, ranges[c])
            if enc in tmp_range:
                current_range = tmp_range
                s += c
                # print(c + str(tmp_range))
                break
        if enc == current_range.get_low():
            break
    if s[-1] == '$':
        s = s[:-1]
    return s


def bound(zip_sym_prob):
    Pr = dict()
    low = 0
    for e in zip_sym_prob:
        high = low + e[1]
        Pr[e[0]] = Range(low, high)
        low = high
    return Pr


def new_range(range_a, range_b):
    new_low = range_a.get_low() + range_a.ampiezza() * range_b.get_low()
    new_high = range_a.get_low() + range_a.ampiezza() * range_b.get_high()
    return Range(mpf(new_low), mpf(new_high))


def split_interval(current_range, zip_sym_prob):
    low = current_range.get_low()
    new_ranges = dict()
    for _s in zip_sym_prob:
        high = low + _s[1] * current_range.ampiezza()
        new_ranges[_s[0]] = Range(low, high)
        low = high
    return new_ranges


def main():
    s = 'aaaabaaaa'
    print('static')
    f, source_s = enc_static(s)
    print(source_s, f)
    print('dynamic')
    a, source_d = enc_dynamic(s)
    print(source_d, a)
    print('static')
    s = dec_static(f, source_s)
    print(s)
    print('dynamic')
    sd = dec_dynamic(a, source_d)
    print(sd)


if __name__ == '__main__':
    main()
    output = encode('ciao come', precision=30)
    print(output)
