# coding=utf-8
from math import log

import matplotlib.pyplot as plt

from .LZ77 import lz77_c
from .LZ78 import encode as lz78_c
from .Lyndon import DeBruijnSequence
from .bwt import encode as bwt_enc


def main():
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    for alphabet_size in range(2, 6):
        lengths = []
        lz77_lengths = []
        lz78_lengths = []
        lz77_lengths_rev = []
        lz78_lengths_rev = []
        lz77_lengths_bwt = []
        lz78_lengths_bwt = []
        a, b = 2, 6
        lengths = list(range(a, b))
        for length in range(a, b):
            word = DeBruijnSequence(alphabet_size, length)
            word = "".join([alphabet[word[i]] for i in range(len(word))])
            lz77word = lz77_c(word)
            lz78word = lz78_c(word)
            lz77_lengths.append(len(lz77word))
            lz78_lengths.append(len(lz78word))

            encoded_sa, _ = bwt_enc(word, True)
            lz77word_bwt = lz77_c(encoded_sa)
            lz78word_bwt = lz78_c(encoded_sa)
            lz77_lengths_bwt.append(len(lz77word_bwt))
            lz78_lengths_bwt.append(len(lz78word_bwt))

            word = word[::-1]
            lz77word_rev = lz77_c(word)
            lz78word_rev = lz78_c(word)
            lz77_lengths_rev.append(len(lz77word_rev))
            lz78_lengths_rev.append(len(lz78word_rev))

        function_ = [n / log(n) for n in range(a, b)]

        fig, ax = plt.subplots()
        ax.plot(lengths, function_, label="n/log(n)")
        ax.plot(lengths, lz77_lengths, label="lz77")
        ax.plot(lengths, lz78_lengths, label="lz78")
        ax.plot(lengths, lz77_lengths_bwt, label="lz77(bwt)")
        ax.plot(lengths, lz78_lengths_bwt, label="lz78(bwt)")
        ax.plot(lengths, lz77_lengths_rev, label="lz77_rev")
        ax.plot(lengths, lz78_lengths_rev, label="lz78_rev")
        ax.set(xlabel='length', ylabel='LZ7*', title=f'|alphabet|={alphabet_size}, lengths in [{a}, {b}]')
        ax.grid()
        ax.legend()
        mng = plt.get_current_fig_manager()
        mng.window.state('zoomed')
        plt.show()


if __name__ == '__main__':
    main()
