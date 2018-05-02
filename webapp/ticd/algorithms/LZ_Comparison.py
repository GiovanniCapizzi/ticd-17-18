# coding=utf-8
import matplotlib.pyplot as plt

from .LZ77 import lz77_c
from .LZ78 import encode as lz78_c
from .Lyndon import DeBruijnSequence


def main():
    alphabet_size = 3
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    lengths = []
    lz77_lengths = []
    lz78_lengths = []
    for lenght in range(2, 20):
        lengths.append(lenght)
        word = DeBruijnSequence(alphabet_size, lenght)
        word = "".join([alphabet[word[i]] for i in range(len(word))])
        lz77word = lz77_c(word)
        lz78word = lz78_c(word)
        lz77_lengths.append(len(lz77word))
        lz78_lengths.append(len(lz78word))


    fig, ax = plt.subplots()
    ax.plot(lengths, lz77_lengths, color='red', label="lz77")
    ax.plot(lengths, lz78_lengths, color='blue', label="lz78")
    ax.set(xlabel='lenght', ylabel='LZ7*', title='')
    ax.grid()

    plt.show()


if __name__ == '__main__':
    main()
