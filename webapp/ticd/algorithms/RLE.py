# coding=utf-8
from typing import Dict, List, Tuple, Union

from .utils import input_example

__algorithm__ = 'Run Length Encoding'
__author__ = "Mirko Avantaggiato"
__group__ = "miscellaneous"


@input_example(input_string_or_list='aaaaaaaaaabbbbb')
def encode(input_string_or_list: Union[str, List[int]]) -> Dict:
    """
    >>> encode("aaaaaaaaaabbbbb")['pairs']
    [('a', 10), ('b', 5)]
    >>> encode([1, 2, 2, 2, 2, 5])['pairs']
    [(1, 1), (2, 4), (5, 1)]
    """
    result: List[Tuple[str, int]] = []
    as_list = list(input_string_or_list) if type(input_string_or_list) == str else input_string_or_list
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


@input_example(encoded='(a , 10), (b , 5)')
def decode(encoded: Union[List[Tuple[str, int]], List[Tuple[int, int]]]) -> str:
    """
    >>> decode([('a', 10), ('b', 5)])
    'aaaaaaaaaabbbbb'
    >>> decode([(1, 1), (2, 4), (5, 1)])
    [1, 2, 2, 2, 2, 5]
    """
    result: List[str] = []
    for item in encoded:
        for _ in range(item[1]):
            result.append(item[0])
    return "".join(result) if type(result[0]) == str else result


def rho(input_string: str) -> int:
    """
    >>> assert rho("aaaaaaaaaabbbbb") == 2
    """
    return len(encode(input_string)['pairs'])


def main():
    string = 'mississippi'
    encoded = encode(string)['pairs']
    print(encoded)
    print(decode(encoded))

    list_ = [1, 2, 2, 2, 2, 5]
    encoded = encode(list_)['pairs']
    print(encoded)
    print(decode(encoded))


if __name__ == '__main__':
    main()
