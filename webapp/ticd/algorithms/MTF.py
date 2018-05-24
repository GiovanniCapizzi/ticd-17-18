# coding=utf-8
from typing import Any, Dict, List

from .utils import input_example

__algorithm__ = "Move To Front"
__author__ = "Mirko Avantaggiato"
__group__ = "miscellaneous"


@input_example(input_string='hello')
def encode_mtf(input_string: str) -> Dict[str, Any]:
    L = input_string
    X = sorted(set(L))
    output = []
    for c in L:
        output.append(X.index(c))
        X.remove(c)
        X.insert(0, c)

    return {
        "output": output,
        "alphabet": " ".join(
                list(
                        map(lambda x: str(ord(x)), sorted(set(input_string)))
                )
        )
    }


@input_example(integer_list='1 1 2 0 3',
               alphabet='101 104 108 111')
def decode_mtf(integer_list: List[int], alphabet: List[str]) -> str:
    alphabet = list(map(chr, [int(i) for i in alphabet]))
    x = alphabet
    tmp: List[str] = [""] * len(integer_list)
    for i in range(0, len(tmp)):
        tmp[i] = x[integer_list[i]]
        j = x[integer_list[i]]
        x.remove(j)
        x.insert(0, j)

    return "".join(tmp)


def main():
    pass


if __name__ == '__main__':
    main()
