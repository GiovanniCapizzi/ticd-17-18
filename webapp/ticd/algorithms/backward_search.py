# -*- coding: utf-8 -*-
# @author Giuseppe Filippone

from collections import Counter


class BackwardSearch():

    def __init__(self, word):
        self.counter = {}
        self.alph = sorted(set(word))
        i = 0
        for c, index in sorted([(c, i) for c, i in zip(word, range(len(word)))]):
            if c not in self.counter:
                self.counter[c] = i
            i += 1
        self.colums = len(word)
        self.occurrences = {}
        for a in self.alph:
            self.occurrences[a] = []
            i = 0
            for c in word:
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
            last = self.colums - 1
        while first <= last and i >= 1:
            c = word[i - 1]
            first = self.counter[c] + self.__occ(c, first - 1)
            last = self.counter[c] + self.__occ(c, last) - 1
            i -= 1
        if first > last:
            raise Exception("No prefix {} found".format(word))
        return (first, last)

    @staticmethod
    def searchin(string, text):
        bs = BackwardSearch(text)
        return bs.search(string)