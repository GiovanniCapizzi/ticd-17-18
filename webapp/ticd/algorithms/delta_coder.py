# -*- coding: utf-8 -*-
# @author Giuseppe Filippone

from math import log2
from typing import List, Dict

from .gamma import encode as gamma_encode, decode as gamma_decode
from .utils import input_example, integers_encode, integers_decode

__author__ = "Giuseppe Filippone"
__algorithm__ = "Delta"
__group__ = "integers"


class DeltaCoder:

    def __init__(self):
        pass

    def __encode(self, integer):
        return gamma_encode([int(log2(integer)) + 1]) + bin(integer)[3:]

    def encode(self, integers):
        encoded = ""
        for integer in integers:
            encoded += self.__encode(integer)
        return encoded

    def decode(self, text):
        i = 0
        decoded = []
        while i < len(text):
            j, N = i, 0
            while i < len(text) and text[i] == "0":
                N += 1
                i += 1
            tmp = i + N + 1
            N = gamma_decode(text[j:tmp])[0] - 1 if len(text[j:tmp]) > 0 else 0
            decoded.append(int("0b1" + text[tmp:tmp + N], 2))
            i = tmp + N
        return decoded


@input_example(integers="21 -1 1 -2 -4 10")
def encode(integers: List[int]) -> Dict[str, str]:
    return {"text": DeltaCoder().encode(integers_encode(integers))}


@input_example(text="0010101011101000110000100010")
def decode(text: str) -> List[int]:
    return integers_decode(DeltaCoder().decode(text))
