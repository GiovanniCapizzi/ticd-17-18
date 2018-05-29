# coding=utf-8
from math import log

from .utils import input_example
from .LZ77 import lz77_encode
from .LZ78 import encode as lz78_c
from .lzss import encode as lzss
from .Lyndon import DeBruijnSequence
from .bwt import encode as bwt_enc
from .gzip import encode as gzip
from dotmap import DotMap

__algorithm__ = "LZ Compare"
__group__ = "LZ"


@input_example(word_length_range="1-15", alphabet_size="3")
def compare(word_length_range: str, alphabet_size: int, reverse_word: bool, bwt_word: bool):
    a, b = [int(x) + 1 for x in word_length_range.split('-')]
    nlog = [n / log(n) for n in range(a, b)]
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    lengths = list(range(a, b))

    lz77_lengths = []
    lz78_lengths = []
    gzip_lengths = []
    lzss_lengths = []

    lz77_lengths_rev = []
    lz78_lengths_rev = []
    gzip_lengths_rev = []
    lzss_lengths_rev = []

    lz77_lengths_bwt = []
    lz78_lengths_bwt = []
    gzip_lengths_bwt = []
    lzss_lengths_bwt = []

    result = DotMap({
        'plot': {
            'y_unit': ' pairs',
            'n/log(n)': nlog
        }
    })

    plot = result.plot

    for length in lengths:
        de_bruijn_word = DeBruijnSequence(alphabet_size, length)
        de_bruijn_word = "".join([alphabet[de_bruijn_word[i]] for i in range(len(de_bruijn_word))])
        lz77word = lz77_encode(de_bruijn_word)
        lz78word = lz78_c(de_bruijn_word)['pairs']
        gzip_word = gzip(de_bruijn_word)['pairs']
        lzss_word = lzss(de_bruijn_word)['pairs']
        lz77_lengths.append(len(lz77word))
        lz78_lengths.append(len(lz78word))
        gzip_lengths.append(len(gzip_word))
        lzss_lengths.append(len(lzss_word))

        if bwt_word:
            encoded_sa = bwt_enc(de_bruijn_word, True)
            lz77word_bwt = lz77_encode(encoded_sa)
            lz78word_bwt = lz78_c(encoded_sa)['pairs']
            gzip_word_bwt = gzip(encoded_sa)['pairs']
            lzss_word_bwt = lzss(encoded_sa)['pairs']
            lz77_lengths_bwt.append(len(lz77word_bwt))
            lz78_lengths_bwt.append(len(lz78word_bwt))
            gzip_lengths_bwt.append(len(gzip_word_bwt))
            lzss_lengths_bwt.append(len(lzss_word_bwt))

        if reverse_word:
            de_bruijn_word_rev = de_bruijn_word[::-1]
            lz77word_rev = lz77_encode(de_bruijn_word_rev)
            lz78word_rev = lz78_c(de_bruijn_word_rev)['pairs']
            gzip_word_rev = gzip(de_bruijn_word_rev)['pairs']
            lzss_word_rev = lzss(de_bruijn_word_rev)['pairs']
            lz77_lengths_rev.append(len(lz77word_rev))
            lz78_lengths_rev.append(len(lz78word_rev))
            gzip_lengths_rev.append(len(gzip_word_rev))
            lzss_lengths_rev.append(len(lzss_word_rev))

    if bwt_word:
        plot.lz77_bwt = lz77_lengths_bwt
        plot.lz78_bwt = lz78_lengths_bwt
        plot.gzip_bwt = gzip_lengths_bwt
        plot.lzss_bwt = lzss_lengths_bwt

    if reverse_word:
        plot.lz77_rev = lz77_lengths_rev
        plot.lz78_rev = lz78_lengths_rev
        plot.gzip_rev = gzip_lengths_rev
        plot.lzss_rev = lzss_lengths_rev

    plot.lengths = lengths
    plot.lz77 = lz77_lengths
    plot.lz78 = lz78_lengths
    plot.lzss = lzss_lengths
    plot.gzip = gzip_lengths

    return result.toDict()
