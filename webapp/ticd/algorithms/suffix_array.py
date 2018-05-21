# coding=utf-8
import random
import string
from ctypes import CDLL, POINTER, c_int
from functools import reduce
from os import path
from typing import List

from .logging_utils import logging

__algorithm__ = 'Suffix Array'
__group__ = "miscellaneous"


def KS(input_string: str) -> List[int]:
    # [2, 1, 4, 4, 1, 4, 4, 1, 3, 3, 1, 0, 0, 0] mississippi
    alphabet = sorted(set(input_string))
    alphabet = {v: k for k, v in zip(range(1, len(alphabet) + 1), alphabet)}
    new_s = [alphabet[input_string[i]] for i in range(len(input_string))] + ([0] * 3)
    try:
        library = CDLL(path.dirname(__file__) + '/compiled_libraries/KS.so')
    except OSError as e:
        logging.critical(e)
        raise

    library.suffixArray.argtypes = [POINTER(c_int), POINTER(c_int), c_int, c_int]
    s1 = (c_int * len(new_s))(*new_s)
    s2 = (c_int * len(new_s))(*([0] * len(new_s)))
    library.suffixArray(s1, s2, len(input_string), len(input_string) + 3)
    return s2[:len(input_string)]


def suffix_array(text):
    sa = [text[i:] for i in range(len(text))]
    ordered = {word: [] for word in set(sa)}
    for pos, word in enumerate(sa):
        ordered[word].append(pos)
    return reduce(list.__add__, map(lambda x: x[1], sorted(ordered.items())))


def calculate(text: str):
    try:
        return KS(text)
    except OSError:
        return suffix_array(text)


def test():
    times = 100
    random_word_length = 1000
    strings = [''.join(random.choices(string.ascii_letters + string.digits, k=random_word_length))
               for _ in range(times)]
    for str_ in strings:
        a = KS(str_)
        b = suffix_array(str_)
        assert a == b


def main():
    test()
    # a = KS("mississippi")
    # print(a)


if __name__ == '__main__':
    main()
