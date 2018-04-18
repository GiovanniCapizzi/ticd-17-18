# -*- coding: utf-8 -*-
# @author Giuseppe Filippone

from math import log2

from .gamma import encode as gamma_encode


class DeltaCoder():

    def __init__(self):
        pass

    def encode(self, integer):
        return gamma_encode(int(log2(integer)) + 1) + bin(integer)[3:]

    def encode_sequence(self, integers):
        encoded = ""
        for integer in integers:
            encoded += self.encode(integer)
        return encoded

    def m_encode(self, integers):
        codewords = {}
        for integer in integers:
            codewords[integer] = self.encode(integer)
        return codewords

    def decode(self, codeword):
        N = 0
        for c in codeword:
            if c == "0":
                N += 1
            else:
                break
        return int("0b1" + codeword[N + N + 1:], 2)

    def decode_text(self, text):
        i = 0
        decoded = []
        while i < len(text):
            N = 0
            while text[i] == "0":
                N += 1
                i += 1
            tmp = i + N + 1
            N = int("0b" + text[i:tmp], 2) - 1
            decoded.append(int("0b1" + text[tmp:tmp + N], 2))
            i = tmp + N
        return decoded

    def m_decode(self, codewords):
        plainwords = {}
        for codeword in codewords:
            plainwords[codeword] = self.decode(codeword)
        return plainwords
