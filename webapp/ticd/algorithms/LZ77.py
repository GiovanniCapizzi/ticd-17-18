# coding=utf-8
from typing import List, Tuple


def _get_index_length(sb: str, lab: str):
    """
    >>> _get_index_length("", "test")
    (0, 0)
    >>> _get_index_length("t", "test")
    (1, 1)
    >>> _get_index_length("t_tes_", "test")
    (4, 3)
    """
    index, tmp = None, None
    for i in range(len(lab)):
        tmp = lab[0:len(lab) - i]
        if tmp in sb:
            index = sb.rindex(tmp)
            break
    if index is None:
        return 0, 0
    else:
        return len(sb) - index, len(tmp)


def encode_lz77(input_string: str, window: int = 16) -> List[Tuple[int, int, str]]:
    """
    >>> encode_lz77("abaababaabb")
    [(0, 0, 'a'), (0, 0, 'b'), (2, 1, 'a'), (3, 2, 'b'), (5, 3, 'b')]
    >>> encode_lz77("010020$0110$$0111", 7)
    [(0, 0, '0'), (0, 0, '1'), (2, 1, '0'), (0, 0, '2'), (2, 1, '$'), (7, 2, '1'), (5, 2, '$'), (6, 3, '1')]
    """
    lab_limit = window
    result: List[Tuple[int, int, str]] = list()
    p, N = 0, len(input_string)
    while p < N:
        sb = input_string[max(0, p - window):p - 1 + 1]
        lab = input_string[p:p + lab_limit]
        distance, length = _get_index_length(sb, lab[0:-1])
        result_ = (distance, length, input_string[p + length])
        result.append(result_)
        p = p + length + 1
    return result


def decode_lz77(input_tuples: List[Tuple[int, int, str]]) -> str:
    """
    >>> decode_lz77([(0, 0, 'a'), (0, 0, 'b'), (2, 1, 'a'), (3, 2, 'b'), (5, 3, 'b')])
    'abaababaabb'
    >>> decode_lz77([(0, 0, '0'), (0, 0, '1'), (2, 1, '0'), (0, 0, '2'), (2, 1, '$'), (7, 2, '1'), (5, 2, '$'), (6, 3, '1')])
    '010020$0110$$0111'
    """
    s, p = [], 0
    for f, l, c in input_tuples:
        s[p:p + l - 1] = s[p - f:p - f + l - 1 + 1]
        s.append(c)
        p = p + l + 1

    return "".join(s)


def main():
    pass


if __name__ == '__main__':
    main()
