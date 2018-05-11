# -*- coding: utf-8 -*-
# @author Giuseppe Filippone

from typing import List, Tuple

__algorithm__ = "LZss"
__group__ = "lz family"


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


def encode(text: str) -> List[Tuple[str]]:
    return LZss.encode(text)


def decode(code: List[Tuple[str]]) -> str:
    return LZss.decode(code)
