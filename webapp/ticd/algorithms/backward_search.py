# -*- coding: utf-8 -*-
# @author Giuseppe Filippone

from typing import Tuple, Dict

from .bwt import encode as bwt_encode, decode as bwt_decode
from .suffix_array import SuffixArray
from .utils import input_example


__author__ = "Giuseppe Filippone"
__algorithm__ = "Backward-Search"
__group__ = "miscellaneous"


class BackwardSearch:

    def __init__(self, text, use_bwt=False):
        self.counter = {}
        if use_bwt:
            self.suffix_array = SuffixArray.calculate(text + ("$" if use_bwt else ""))
            text = bwt_encode(text, use_suffix_array=True)
        else:
            self.suffix_array = SuffixArray.calculate(bwt_decode(text) + "$")
        self.alph = sorted(set(text))
        i = 0
        for c, index in sorted([(c, i) for c, i in zip(text, range(len(text)))]):
            if c not in self.counter:
                self.counter[c] = i
            i += 1
        self.columns = len(text)
        self.occurrences = {}
        for a in self.alph:
            self.occurrences[a] = []
            i = 0
            for c in text:
                if c == a:
                    i += 1
                self.occurrences[a].append(i)

    def __occ(self, c, index):
        return self.occurrences[c][index]

    def search(self, word):
        i = len(word) - 1
        c = word[i]
        j = self.alph.index(c)
        first, last = self.counter[c], self.counter[self.alph[(j + 1) % len(self.alph)]] - 1
        if last < first:
            last = self.columns - 1
        while first <= last and i >= 1:
            c = word[i - 1]
            first = self.counter[c] + self.__occ(c, first - 1)
            last = self.counter[c] + self.__occ(c, last) - 1
            i -= 1
        if first > last:
            return (-1, [])
        return (last - first + 1, sorted([self.suffix_array[i] for i in range(first, last + 1)]))

    @staticmethod
    def searchin(string, text):
        return BackwardSearch(text, True).search(string)


@input_example(text="hellodasdahellodada", word="hello")
def search(word: str, text: str, text_is_bwt: bool=False) -> Dict:
    occ, pos = BackwardSearch.searchin(word, text) if not text_is_bwt else BackwardSearch(text, False).search(word)
    if occ > 0:
        return {"occurences": occ, "positions": pos} 
    else:
        return {"error": f"{word} not found"} 
