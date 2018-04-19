# coding=utf-8
"""
Sardinas-Patterson algorithm.
"""
from typing import Tuple, Union


class Code(object):
    """
    Class for Code.
    """

    def __init__(self, words: set):
        self.words = words

    def __str__(self):
        return self.words.__str__()

    def __eq__(self, other):
        return self.words.__eq__(other)

    def __neq__(self, other):
        return not self.__eq__(other)


def is_proper_prefix(s: str, word: str) -> bool:
    """
    This method test is `s` is a proper prefix of `word`.
    >>> is_proper_prefix("test", "test")
    False
    >>> is_proper_prefix("test", "test_")
    True
    """
    return word.startswith(s) and s != word


def sardinas_patterson(code: Code) -> Union[Tuple[bool, str, set], Tuple[bool, str], Tuple[bool, str, str]]:
    """
    SardinasPatterson algorithm.
    :param code:
    :return:
    """

    def find_suffixes(s_i: Code, s_i1: Code) -> set:
        """
        :param s_i:
        :param s_i1: s_{i-1}
        :return:
        """
        _result = set()
        for w in s_i.words:
            for v in s_i1.words:
                if is_proper_prefix(w, v):
                    _result.add(v[len(w):])
        return _result

    s = [code, Code(find_suffixes(code, code))]
    print("s_{} = {}".format(0, s[0]))
    print("s_{} = {}".format(1, s[1]))
    if s[1] == set():
        return True, "Empty set found!", "Prefix Code - Decoding delay LIMITED"

    i = 2
    while True:
        result = Code(find_suffixes(s[i - 1], s[0]) | find_suffixes(s[0], s[i - 1]))
        print("s_{} = {}".format(i, result))
        intersection = result.words.intersection(s[0].words)
        if len(intersection) != 0:
            return False, "Intersection with s_0 not empty!", intersection
        if len(result.words) == 0:
            return True, "Empty set found!", "Decoding delay LIMITED"
        for _s in s:
            if _s.words == result:
                return True, "Duplicate set found!", "Decoding delay UNLIMITED"

        s.append(result)
        i += 1


def main():
    """
    Examples.
    """
    print(sardinas_patterson(Code({"a", "c", "ad", "abb", "bad", "deb", "bbcde"})))
    print(sardinas_patterson(Code({"abc", "abcd", "e", "dba", "bace", "ceac", "ceab", "eabd"})))
    print(sardinas_patterson(Code({"010", "0001", "0110", "1100", "00011", "00110", "11110", "101011"})))
    print(sardinas_patterson(Code({"0", "01", "10", "1"})))
    print(sardinas_patterson(Code({"00", "01", "10", "11"})))
    print(sardinas_patterson(Code({"0", "10", "10", "11"})))


if __name__ == '__main__':
    main()
