# -*- coding: utf-8 -*-
# @author Giuseppe Filippone

from typing import Set, Tuple


__algorithm__ = "Arithmetic Coding Adaptive"
__group__ = "miscellaneous"


def prefix(a, b):
    pref = ""
    for x, y in zip(str(a), str(b)):
        if x != y:
            break
        pref += x
    return pref


class ArithmeticCoder:

    def encode(self, alphabet, text):
        n = len(alphabet)
        encoded = "0."
        low, high = 0.0, 1.0
        counter = {a: 1 for a in alphabet}

        def bound(x):
            return counter[x] * (high - low) / n

        sort_alpha = sorted([k for k in alphabet])

        for character in text:
            lower = low
            for k in sort_alpha:
                if k == character:
                    high = lower + bound(k)
                    counter[k], n = counter[k] + 1, n + 1
                    break
                lower += bound(k)
            low = lower
            pref = prefix(low, high)
            if len(pref) > 2:
                encoded += pref[2:]
                low = float("0." + str(low)[len(pref):])
                high = float("0." + str(high)[len(pref):])
        pref = prefix(low, high)[:2]
        return encoded + str(low)[len(pref):], encoded + str(high)[len(pref):]

    def decode(self, codeword, alphabet):
        n = len(alphabet)
        low, high = 0.0, 1.0
        decodedword = b""
        lw, hg = codeword
        counter = {a: 1 for a in alphabet}

        def bound(x):
            return counter[x] * (high - low) / n

        sort_alpha = sorted([k for k in alphabet])

        while True:
            lower = low
            for k in sort_alpha:
                bk = bound(k)
                if str(lower) <= lw < str(lower + bk):
                    high = lower + bk
                    decodedword += k
                    if (lw, hg) == (str(lower), str(high)):
                        return decodedword
                    counter[k], n = counter[k] + 1, n + 1
                    break
                lower += bk
            low = lower
            pref = prefix(low, high)
            if len(pref) > 2:
                lw, hg = "0." + lw[len(pref):], "0." + hg[len(pref):]
                low = float("0." + str(low)[len(pref):])
                high = float("0." + str(high)[len(pref):])


def encode(alphabet: Set[str], text: str) -> Tuple[str]:
    return ArithmeticCoder().encode(alphabet, text)


def decode(codeword: Tuple[str, str], alphabet: Set[str]) -> str:
    return ArithmeticCoder().decode(codeword, alphabet)
