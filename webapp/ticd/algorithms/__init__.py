# coding=utf-8
import sys
from . import unary_coding

tmp = dir(sys.modules[__name__])
algorithms_list = {
    'GZIP': None,
    'LZW': None,
    'Unary': unary_coding,
    'Gamma': None,
    'Delta': None,
    'Fibonacci': None,
    'Levenshtein': None,
    'RLE': None
}
algorithms = {
    'LZ Family': ['GZIP', 'LZW'],
    'Integers': ['Unary', 'Gamma', 'Delta', 'Fibonacci', 'Levenshtein ', 'RLE']
}
