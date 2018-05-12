from .LZ77 import lz77_encode
from .LZ78 import encode as lz78_c
from .Lyndon import DeBruijnSequence
from .bwt import encode as bwt_enc
from math import log

__algorithm__ = "Compare"
__group__ = "LZ"


def compare(word_length_range: str, alphabet_size: int):
    a, b = [int(x)+1 for x in word_length_range.split('-')]
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    lengths = list(range(a, b))

    lz77_lengths = []
    lz78_lengths = []
    lz77_lengths_rev = []
    lz78_lengths_rev = []
    lz77_lengths_bwt = []
    lz78_lengths_bwt = []

    for length in lengths:
        de_bruijn_word = DeBruijnSequence(alphabet_size, length)
        de_bruijn_word = "".join([alphabet[de_bruijn_word[i]] for i in range(len(de_bruijn_word))])
        lz77word = lz77_encode(de_bruijn_word)
        lz78word = lz78_c(de_bruijn_word)['pairs']
        lz77_lengths.append(len(lz77word))
        lz78_lengths.append(len(lz78word))

        encoded_sa = bwt_enc(de_bruijn_word, True)
        lz77word_bwt = lz77_encode(encoded_sa)
        lz78word_bwt = lz78_c(encoded_sa)['pairs']
        lz77_lengths_bwt.append(len(lz77word_bwt))
        lz78_lengths_bwt.append(len(lz78word_bwt))

        de_bruijn_word_rev = de_bruijn_word[::-1]
        lz77word_rev = lz77_encode(de_bruijn_word_rev)
        lz78word_rev = lz78_c(de_bruijn_word_rev)['pairs']
        lz77_lengths_rev.append(len(lz77word_rev))
        lz78_lengths_rev.append(len(lz78word_rev))

        nlog = [n / log(n) for n in range(a, b)]

    return {
        'plot': {
            'lengths': lengths,
            'lz77': lz77_lengths,
            'lz77-bwt': lz77_lengths_bwt,
            'lz78-bwt': lz78_lengths_bwt,
            'lz78-rev': lz78_lengths_rev,
            'lz77-rev': lz77_lengths_rev,
            'n/log(n)': nlog
        }
    }
