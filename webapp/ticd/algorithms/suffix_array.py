# coding=utf-8
import random
import string
from ctypes import CDLL, POINTER, c_int
from functools import reduce
from typing import List

from .logging_utils import logging


def KS(s: str) -> List[int]:
    # [2, 1, 4, 4, 1, 4, 4, 1, 3, 3, 1, 0, 0, 0] mississippi
    alphabet = sorted(set(s))
    alphabet = {v: k for k, v in zip(range(1, len(alphabet) + 1), alphabet)}
    new_s = [alphabet[s[i]] for i in range(len(s))] + ([0] * 3)
    library = None
    try:
        library = CDLL('webapp/ticd/algorithms/compiled_libraries/KS.so')
    except OSError as e:
        logging.critical(e)
        exit(1)

    library.suffixArray.argtypes = [POINTER(c_int), POINTER(c_int), c_int, c_int]
    library.suffixArray.restype = c_int
    s1 = (c_int * len(new_s))(*new_s)
    s2 = (c_int * len(new_s))(*([0] * len(new_s)))
    library.suffixArray(s1, s2, len(s), len(s) + 3)
    return s2[:len(s)]


def suffix_array(text):
    sa = [text[i:] for i in range(len(text))]
    ordered = {word: [] for word in set(sa)}
    for pos, word in enumerate(sa):
        ordered[word].append(pos)
    return reduce(list.__add__, map(lambda x: x[1], sorted(ordered.items())))


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
