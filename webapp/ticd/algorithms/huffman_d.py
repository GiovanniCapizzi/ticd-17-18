# coding=utf-8
import queue
from collections import Counter
from math import ceil
from typing import Dict

import networkx as nx

from .utils import input_example, plot_tree

__algorithm__ = 'Huffman'
__group__ = "miscellaneous"
__author__ = 'Giovanni Capizzi'


class Node:
    def __init__(self, c, p, children=None):
        self.c = c  # Character
        self.p = p  # Probability
        # List of Nodes
        self.children = children

    # Required for Priority Queue
    def __lt__(self, other):
        return self.p < other.p

    # To String
    def __str__(self):
        return self.c
        # return "(%s %s)" % (self.c, self.p)

    def __repr__(self):
        return str(self)


def graph_maker(node, v_graph):
    # is an internal node so
    for i, child in enumerate(node.children):
        if child.children is None:
            v_graph.add_edge(node, child)
        else:
            v_graph.add_edge(node, child, length=100)
            graph_maker(child, v_graph)


def generate_graph(node):
    g = nx.Graph()
    graph_maker(node, g)
    return plot_tree(g, node)


# Extract the encoding dict
def code_maker(node, index, encode_by):
    if type(index) is not str:
        return
    # index is used for building the
    # code string during the tree exploration
    if node.children is None:
        encode_by[node.c] = index
    else:
        # is an internal node so
        for i, child in enumerate(node.children):
            code_maker(child, index + str(i), encode_by)


@input_example(d='2', text='mississippi')
def encode(d: int, text: str):
    # Text Length
    length = len(text)
    # Queue
    pq = queue.PriorityQueue()
    # Produced encoding dict
    encode_by = {}
    # Frequency Dict
    freq = Counter(text)
    freq_len = len(freq)
    if freq_len == 1:
        coded = freq[text[0]]
        patch = {text[0]: '0'}
        return {
            'encoded': '0'*coded,
            'codebook': patch,
            'edges': None
        }

    # print("Numero di simboli", freq_len, "prima del fix")

    # Fix Nodes
    x = int(ceil((len(freq) - d) / (d - 1)))
    fake_nodes = (d + x * (d - 1)) - freq_len
    for i in range(fake_nodes):
        pq.put(Node("fake" + str(i), 0.0))

    # Enqueuing all nodes
    for key, value in freq.items():
        pq.put(Node(key, round(value / length, 5)))

    # print("Numero di simboli", pq.qsize(), "dopo il fix")

    counter = 0

    # Group them by d elements
    while pq.qsize() >= d:
        # Take d nodes
        group = [pq.get() for _ in range(d)]
        # For each Node n in group
        probabilities = map(lambda n: n.p, group)
        pq.put(Node(f'in{counter}', sum(probabilities), group))
        counter += 1

    # Creating the relative code
    root = pq.get()

    code_maker(root, "", encode_by)
    encoded = ""
    for c in text:
        encoded += encode_by[c]

    encode_by = dict(filter(lambda t: 'fake' not in t[0], encode_by.items()))

    return {
        'encoded': encoded,
        'codebook': encode_by,
        'edges': generate_graph(root)
    }


@input_example(encoded='100011110111101011010,',
               codebook='{"i":"0","m":"100","p":"101","s":"11"}')
def decode(encoded: str, codebook: Dict):

    decode_by = {v: k for k, v in codebook.items()}
    # Decoding
    buffer = ""
    output = ""
    for encoded_char in encoded:
        buffer += encoded_char
        if buffer in decode_by.keys():
            output += decode_by[buffer]
            buffer = ""
    return output


if __name__ == '__main__':
    in_text = "La signora Aurora si ricorda che Mario cerca Giacomino ogni giorno alle 14"
    #in_text = "aaaaaaaaaa"
    output = encode(2, in_text)
    print(output['encoded'], "\n", output['codebook'])
    print(decode(output['encoded'], output['codebook']))

