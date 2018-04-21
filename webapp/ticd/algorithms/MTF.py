# coding=utf-8
import random
import string
from typing import List


def mtf(s: str) -> List[int]:
    L = s
    X = sorted(set(L))
    output = []
    for c in L:
        output.append(X.index(c))
        X.remove(c)
        X.insert(0, c)

    return output


def mtf_i(r: List[int], alphabet: List[str]) -> str:
    x = alphabet
    tmp: List[str] = [""] * len(r)
    for i in range(0, len(tmp)):
        tmp[i] = x[r[i]]
        j = x[r[i]]
        x.remove(j)
        x.insert(0, j)

    return "".join(tmp)


def test():
    for _ in range(100):
        w = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(128))
        alphabet = sorted(set(w))
        encoded = mtf(w)
        decoded = mtf_i(encoded, alphabet)
        assert w == decoded


def main():
    test()


if __name__ == '__main__':
    main()
