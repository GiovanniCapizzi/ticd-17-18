# coding=utf-8
import random
import string
from typing import List

__algorithm__ = "Move To Front"
__group__ = "miscellaneous"


def encode_mtf(input_string: str) -> List[int]:
    L = input_string
    X = sorted(set(L))
    output = []
    for c in L:
        output.append(X.index(c))
        X.remove(c)
        X.insert(0, c)

    return output


def decode_mtf(integer_list: List[int], alphabet: List[str]) -> str:
    x = alphabet
    tmp: List[str] = [""] * len(integer_list)
    for i in range(0, len(tmp)):
        tmp[i] = x[integer_list[i]]
        j = x[integer_list[i]]
        x.remove(j)
        x.insert(0, j)

    return "".join(tmp)


def test():
    for _ in range(100):
        w = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(128))
        alphabet = sorted(set(w))
        encoded = encode_mtf(w)
        decoded = decode_mtf(encoded, alphabet)
        assert w == decoded


def main():
    test()


if __name__ == '__main__':
    main()
