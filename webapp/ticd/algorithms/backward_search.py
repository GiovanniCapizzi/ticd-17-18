# -*- coding: utf-8 -*-
# @author Giuseppe Filippone

from typing import Tuple, Dict

from .bwt import encode as bwt_encode

__algorithm__ = "Backward-Search"
__group__ = "miscellaneous"


class BackwardSearch:

    def __init__(self, text, use_bwt=False):
        self.counter = {}
        if use_bwt:
            text = bwt_encode(text, use_suffix_array=True)
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
            return -1, -1
        return first, last

    @staticmethod
    def searchin(string, text):
        bs = BackwardSearch(text, True)
        return bs.search(string)


def search(word: str, text: str, text_is_bwt: bool=False) -> Dict:
    first, last = BackwardSearch.searchin(word, text) if not text_is_bwt else BackwardSearch(text, False).search(word)
    if (first, last) != (-1, -1):
        return {"occurences": last - first + 1, "positions": (first, last)} 
    else:
        return {"error": f"{word} not found"} 
