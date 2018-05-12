# coding=utf-8
from typing import List, Tuple, Dict


def encode(input_string: str) -> Dict:
    """
    >>> encode("aaaaaaaaaabbbbb")
    [('a', 10), ('b', 5)]
    """
    result: List[Tuple[str, int]] = []
    as_list = list(input_string)
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

    return {'pairs': result}


def decode(encoded: List[Tuple[str, int]]) -> str:
    """
    >>> decode([('a', 10), ('b', 5)])
    'aaaaaaaaaabbbbb'
    """
    result: List[str] = []
    for item in encoded:
        result.append(item[0] * item[1])
    return "".join(result)


def rho(input_string: str) -> int:
    """
    >>> assert rho("aaaaaaaaaabbbbb") == 2
    """
    return len(rle(input_string))


def main():
    s = "aabbbaabbbbbbaaabbaaaa"
    encoded = encode(s)
    decoded = decode(encoded)
    print(s, encoded, decoded)
    print(rho(s))


if __name__ == '__main__':
    main()
