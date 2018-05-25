# coding=utf-8

from .Lyndon import DeBruijnSequence
from .bwt import encode as bwt_enc
from .fgk import encode as fgk
from .huffman_d import encode as huffman
from .utils import input_example

__algorithm__ = "Huffman Compare"
__group__ = "miscellaneous"


@input_example(word_length_range="1-15", alphabet_size="3")
def compare(word_length_range: str, alphabet_size: int):
    a, b = [int(x) + 1 for x in word_length_range.split('-')]
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    lengths = list(range(a, b))

    huffman_lengths = []
    fgk_lengths = []
    huffman_bwt_lengths = []
    fgk_bwt_lengths = []

    for length in lengths:
        de_bruijn_word = DeBruijnSequence(alphabet_size, length)
        de_bruijn_word = "".join([alphabet[de_bruijn_word[i]] for i in range(len(de_bruijn_word))])
        bwt_word = bwt_enc(de_bruijn_word, True)
        fgk_word = fgk(de_bruijn_word)['sequence']
        fgk_word_bwt = fgk(bwt_word)['sequence']

        huffman_word = huffman(2, de_bruijn_word)
        huff_word = huffman_word['encoded']
        huff_dict = huffman_word['codebook']

        huffman_word_bwt = huffman(2, bwt_word)
        huff_bwt_word = huffman_word_bwt['encoded']
        bwt_dict = huffman_word_bwt['codebook']

        huff_dict = len(huff_dict) * 4 + sum(len(x) for x in huff_dict.values())
        bwt_dict = len(bwt_dict) * 4 + sum(len(x) for x in bwt_dict.values())

        huffman_lengths.append(len(huff_word) + huff_dict)
        huffman_bwt_lengths.append(len(huff_bwt_word) + bwt_dict)
        fgk_lengths.append(len(fgk_word))
        fgk_bwt_lengths.append(len(fgk_word_bwt))

    return {
        'plot': {
            'y_unit': ' bit',
            'lengths': lengths,
            'huffman': huffman_lengths,
            'huffman_bwt': huffman_bwt_lengths,
            'fgk': fgk_lengths,
            'fgk_bwt': fgk_bwt_lengths,
        }
    }
