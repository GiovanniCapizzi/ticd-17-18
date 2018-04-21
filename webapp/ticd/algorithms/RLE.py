# coding=utf-8
from typing import List, Tuple


def rle(s: str) -> List[Tuple[str, int]]:
    """
    >>> rle("aaaaaaaaaabbbbb")
    [('a', 10), ('b', 5)]
    """
    result: List[Tuple[str, int]] = []
    as_list = list(s)
    counter = 0
    prev = as_list[0]
    while len(as_list) != 0:
        if as_list[0] == prev:
            counter += 1
            as_list.pop(0)
        else:
            result.append((prev, counter))
            counter = 0
            prev = as_list[0]
    result.append((prev, counter))

    return result


def rle_i(encoded: List[Tuple[str, int]]) -> str:
    """
    >>> rle_i([('a', 10), ('b', 5)])
    'aaaaaaaaaabbbbb'
    """
    result: List[str] = []
    for item in encoded:
        result.append(item[0] * item[1])
    return "".join(result)


def rho(s: str) -> int:
    """
    >>> assert rho("aaaaaaaaaabbbbb") == 2
    """
    return len(rle(s))


def main():
    s = "aabbbaabbbbbbaaabbaaaa"
    encoded = rle(s)
    decoded = rle_i(encoded)
    print(s, encoded, decoded)
    print(rho(s))


if __name__ == '__main__':
    main()
