# -*- coding: utf-8 -*-
# @author Giuseppe Filippone

from re import sub
from typing import Dict, List, Tuple

from .utils import input_example

__author__ = "Giuseppe Filippone"
__algorithm__ = "LZss"
__group__ = "LZ"


class LZss(object):

    @staticmethod
    def encode(text):
        encoded = []
        j, ilcp = 0, 0
        while j < len(text):
            jj, lenlcp, ilcp = 1, 0, 0
            while j + jj <= len(text):
                try:
                    pattern = text[j:(j + jj)]
                    index = text[:(j + jj - 1)].rindex(pattern)
                    if len(pattern) >= lenlcp:
                        ilcp = index
                        lenlcp = len(pattern)
                    jj += 1
                except Exception as e:
                    break
            if lenlcp == 0:
                encoded.append((0, text[j]))
                j += 1
            else:
                encoded.append(((j - ilcp), lenlcp))
                j += lenlcp
        return encoded

    @staticmethod
    def decode(code):
        decoded = ""
        for i in range(0, len(code)):
            distance, lenlcp_character = code[i]
            if distance != 0:
                lenlcp = int(lenlcp_character)
                character = ""
            else:
                lenlcp = 0
                character = lenlcp_character

            if distance == 0:
                decoded += character
            elif lenlcp <= distance:
                decoded += decoded[-distance:][:lenlcp]
            else:
                tmp = decoded[-distance:]
                for j in range(lenlcp):
                    decoded += tmp[j % len(tmp)]
                decoded += character
        return decoded


@input_example(text="mississippi")
def encode(text: str) -> Dict:
    return {'pairs': LZss.encode(text)}


@input_example(code="(0 , m),(0 , i),(0 , s),(1 , 1),(3 , 4),(0 , p),(1 , 1),(3 , 1)")
def decode(code: List[Tuple[int, str]]) -> str:
    return LZss.decode(code)
