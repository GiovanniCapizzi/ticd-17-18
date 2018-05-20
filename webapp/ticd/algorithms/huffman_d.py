# coding=utf-8
import queue
from collections import Counter
from math import ceil
from typing import Dict
import matplotlib.pyplot as plt
import networkx as nx

# matplotlib.use("Agg")


__algorithm__ = 'Huffman'
__group__ = "miscellaneous"


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
        return ""
        # return "(%s %s)" % (self.c, self.p)

    def __repr__(self):
        return str(self)


def graph_maker(node, v_graph):
    # is an internal node so
    for i, child in enumerate(node.children):
        if child.children is None:
            v_graph.add_edge(node, child.c)
        else:
            v_graph.add_edge(node, child, length=100)
            graph_maker(child, v_graph)


def generate_graph(node, path=''):
    g = nx.Graph()
    graph_maker(node, g)
    return g.edges()

    # f = plt.figure()
    # pos = nx.spring_layout(g, k=0.15, iterations=500)
    # nx.draw(g, ax=f.add_subplot(111), with_labels=True, pos=pos)
    # f.savefig(path)


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


def encode(d: int, text: str, path=''):
    # Text Length
    length = len(text)
    # Queue
    pq = queue.PriorityQueue()
    # Produced encoding dict
    encode_by = {}
    # Frequency Dict
    freq = Counter(text)
    freq_len = len(freq)

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

    # Group them by d elements
    while pq.qsize() >= d:
        # Take d nodes
        group = [pq.get() for _ in range(d)]
        # For each Node n in group
        probabilities = map(lambda n: n.p, group)
        pq.put(Node("Internal Node", sum(probabilities), group))

    # Creating the relative code
    root = pq.get()



    code_maker(root, "", encode_by)
    encoded = ""
    for c in text:
        encoded += encode_by[c]

    encode_by = dict(filter(lambda t: 'fake' not in t[0], encode_by.items()))
    edges = generate_graph(root)



    return {
        'encoded': encoded,
        'codebook': encode_by,
        'edges': edges
    }


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


def main():
    in_text = "La signora Aurora si ricorda che Mario cerca Giacomino ogni giorno alle 14"
    output = encode(4, in_text, "D:\\graph.jpg")
    print(output['encoded'], "\n", output['codebook'])
    print(decode(output['encoded'], output['codebook']))


if __name__ == '__main__':
    main()
