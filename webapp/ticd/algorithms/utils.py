# coding=utf-8
import time
from os import makedirs, path, remove, walk
from random import randint

import networkx as nx
from django.utils.crypto import get_random_string
from matplotlib import pyplot
from networkx.drawing.nx_pydot import graphviz_layout


class timer(object):
    def __init__(self, operation_name=""):
        self.name = operation_name
        self.start_time = None

    def __enter__(self):
        self.start_time = time.time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.total_time = time.time() - self.start_time
        if self.name != "":
            print("Total time for {}: {}s".format(self.name, self.total_time))
        else:
            print("Total time: {}s".format(self.total_time))


def open_file(file_name, size=None):
    with open(file_name) as f:
        lines = f.readlines()
        if size is None:
            size = len(lines)
        lines = ''.join(lines[:size])
    return lines


def SturmGen(d_n, max_random):
    d_list = [randint(0, max_random)] + [randint(1, max_random) for _ in range(d_n)]

    S0 = '0'
    S1 = '1'

    for i in range(len(S1), d_n + 1):
        temp = S1
        S1 = S1 * d_list[i] + S0
        S0 = temp

    return S1


directory = path.join(path.dirname(__file__), '../static/plot/')


def save_tree():
    if not path.exists(directory):
        makedirs(directory)

    for root, dirs, files in walk(directory):
        for filename in files:
            remove(path.join(root, filename))

    name = get_random_string(32) + '.png'
    pyplot.savefig(directory + name, dpi=300)
    return name


def plot_tree(g, root):
    pyplot.cla()
    pyplot.clf()

    edge_labels = {}
    all_nodes = []
    nodes = [root]
    while len(nodes) > 0:
        node = nodes.pop(0)
        if node.children is not None:
            all_nodes.append(node)
            i = 0
            for child in node.children:
                nodes.append(child)
                edge_labels[(node, child)] = str(i)
                i += 1

    pos = graphviz_layout(nx.bfs_tree(g, root), prog='dot', root=root)
    node_labels = dict([(v, v.c if len(v.c) == 1 else "") for v in g.nodes()])
    node_sizes = [len(v) * 150 if len(v) > 0 else 40 for _, v in node_labels.items()]
    nx.draw_networkx_edges(g, pos)
    nxnodes = nx.draw_networkx_nodes(g, pos, node_size=node_sizes, node_color="w")
    nxnodes.set_edgecolor('k')
    nx.draw_networkx_edge_labels(g, pos, font_size=8, edge_labels=edge_labels)
    nx.draw_networkx_labels(g, pos, font_color="k", font_size=8, labels=node_labels)
    pyplot.axis('off')

    del edge_labels, all_nodes, nodes
    return save_tree()


def encode_numbers(integers):
    return list(map(lambda number: number * 2 if number >= 0 else -number * 2 + 1, integers))


def decode_numbers(integers):
    return list(map(lambda number: int(number / 2 if not number % 2 else (number - 1) / -2), integers))


class input_example(object):
    """
    @input_example(list_of_integers="46 33 13 1 48 23 34 13 15 3")
    def encode_unary(list_of_integers: List[int]) -> str:
        ...

    print(encode_unary.input_example)
    """

    def __init__(self, *args, **kwargs):
        self.input_example = kwargs

    def __call__(self, *args, **kwargs):
        args[0].input_example = self.input_example
        return args[0]


if __name__ == '__main__':
    with timer():
        time.sleep(1)
