# coding=utf-8
from typing import Dict, List

from mpmath import mp, mpf

mp.prec = 80  # 1000000


# increase value up to very high values to increase precision

def entropy_from_prob_list(p_list, base: int = 2) -> float:
    """
    This method returns entropy from a probabilities list.
    \sum ( p_i log_2(1 / p_i) )

    :param p_list: probabilities
    :param base: logarithm base
    :return: entropy
    """
    entropy = 0
    for p in p_list:
        entropy += p * log(1 / p, base)
    return entropy


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


def encode_dyn(s: str) -> (List[str], mpf):
    """
    >>> encode_dyn('aaaabaaaa')
    (['$', 'a', 'b'], mpf('0.5263107263107262766304979'))
    """
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
    return A, current_range.get_low()


def decode_dyn(enc: mpf, list_sym: list) -> str:
    """
    >>> decode_dyn(mpf('0.5263107263107262766304979'), ['$', 'a', 'b'])
    'aaaabaaaa'
    """
    current_range = Range(mpf(0), mpf(1))
    A = sorted(list_sym)
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


def encode_s(s: str) -> (Dict[str, mpf], mpf):
    """
    >>> encode_s('aaaabaaaa')
    ({'a': 0.7999999999999999, 'b': 0.1, '$': 0.1}, mpf('0.67593139199999975394545314'))
    """
    s += '$'
    source = source_prob(s)
    current_range = Range(mpf(0), mpf(1))
    tmp = sorted(zip(source.keys(), source.values()))
    ranges = bound(tmp)
    for c in s:
        current_range = new_range(current_range, ranges[c])
    return source, current_range.get_low()


def decode_s(enc: mpf, source: dict) -> str:
    """
    >>> decode_s(mpf('0.67593139199999975394545314'), {'a': 0.7999999999999999, 'b': 0.1, '$': 0.1})
    'aaaabaaaa'
    """
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
    source_s, f = encode_s(s)
    print(source_s, f)
    print('dynamic')
    source_d, a = encode_dyn(s)
    print(source_d, a)
    print('static')
    s = decode_s(f, source_s)
    print(s)
    print('dynamic')
    sd = decode_dyn(a, source_d)
    print(sd)


if __name__ == '__main__':
    main()
