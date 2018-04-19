# coding=utf-8
from typing import List


def mtf(s: str) -> List[int]:
    L = s
    X = list(sorted(list(set(L))))
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


def main():
    w = "broood"
    encoded = mtf(w)
    decoded = mtf_i(encoded, sorted(set(w)))
    print(encoded, decoded)


if __name__ == '__main__':
    main()
