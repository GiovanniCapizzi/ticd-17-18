from random import randint

from .delta_coder import encode as delta_encode
from .fibonacci import encode as fib_encode
from .gamma import encode as gamma_encode
from .levenshtein_coding import encode as lv_encode
from .unary_coding import encode_unary as unary_encode

__algorithm__ = "Compare"
__group__ = "integers"


def compare(integers_count: str):
    a, b = [int(x) + 1 for x in integers_count.split('-')]
    lengths = []

    fib_lengths = []
    lev_lengths = []
    gamma_lengths_ = []
    delta_lengths = []
    unary_lengths = []

    for length in range(a, b, 100):
        word = [randint(1, 300) for _ in range(length)]
        lengths.append(len(word) * 4 * 8)

        fibonacci = fib_encode(word)
        lev = lv_encode(word)
        gamma = gamma_encode(word)
        delta = delta_encode(word)
        unary = unary_encode(word)

        fib_lengths.append(len(fibonacci))
        lev_lengths.append(len(lev))
        gamma_lengths_.append(len(gamma))
        delta_lengths.append(len(delta))
        unary_lengths.append(len(unary))

    return {
        'plot': {
            'lengths': lengths,
            'fibonacci': fib_lengths,
            'levenshtein': lev_lengths,
            'gamma': gamma_lengths_,
            'delta': delta_lengths,
            'unary': unary_lengths
        }
    }