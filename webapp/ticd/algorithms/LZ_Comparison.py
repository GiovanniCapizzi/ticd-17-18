# coding=utf-8
from math import log

import matplotlib.pyplot as plt

from .LZ77 import lz77_c
from .LZ78 import encode as lz78_c
from .Lyndon import DeBruijnSequence
from .bwt import encode as bwt_enc
from .utils import SturmGen, timer


def main():
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    a, b = 2, 10
    lengths = list(range(a, b))
    for alphabet_size in range(2, 6):
        lz77_lengths = []
        lz78_lengths = []
        lz77_lengths_rev = []
        lz78_lengths_rev = []
        lz77_lengths_bwt = []
        lz78_lengths_bwt = []

        for length in range(a, b):
            with timer("LZ77\\LZ77(DeBruijn)"):
                de_bruijn_word = DeBruijnSequence(alphabet_size, length)
                de_bruijn_word = "".join([alphabet[de_bruijn_word[i]] for i in range(len(de_bruijn_word))])
                lz77word = lz77_c(de_bruijn_word)
                lz78word = lz78_c(de_bruijn_word)
                lz77_lengths.append(len(lz77word))
                lz78_lengths.append(len(lz78word))

            with timer("LZ77\\78(bwt(DeBruijn))"):
                encoded_sa, _ = bwt_enc(de_bruijn_word, True)
                lz77word_bwt = lz77_c(encoded_sa)
                lz78word_bwt = lz78_c(encoded_sa)
                lz77_lengths_bwt.append(len(lz77word_bwt))
                lz78_lengths_bwt.append(len(lz78word_bwt))

            with timer("LZ77\\78(rev(DeBruijn))"):
                de_bruijn_word_rev = de_bruijn_word[::-1]
                lz77word_rev = lz77_c(de_bruijn_word_rev)
                lz78word_rev = lz78_c(de_bruijn_word_rev)
                lz77_lengths_rev.append(len(lz77word_rev))
                lz78_lengths_rev.append(len(lz78word_rev))

        function_ = [n / log(n) for n in range(a, b)]

        fig, ax = plt.subplots()
        ax.plot(lengths, function_, label="n/log(n)")
        ax.plot(lengths, lz77_lengths, label="lz77(DeBruijn)")
        ax.plot(lengths, lz78_lengths, label="lz78(DeBruijn)")
        ax.plot(lengths, lz77_lengths_bwt, label="lz77(bwt(DeBruijn))")
        ax.plot(lengths, lz78_lengths_bwt, label="lz78(bwt(DeBruijn))")
        ax.plot(lengths, lz77_lengths_rev, label="lz77(rev(DeBruijn))")
        ax.plot(lengths, lz78_lengths_rev, label="lz78(rev(DeBruijn))")
        ax.set(xlabel='length', ylabel='LZ7*', title=f'|alphabet|={alphabet_size}, lengths in [{a}, {b}]')
        ax.grid()
        ax.legend()
        mng = plt.get_current_fig_manager()
        mng.window.state('zoomed')
        plt.show()


if __name__ == '__main__':
    main()
