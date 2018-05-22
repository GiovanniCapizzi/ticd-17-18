# coding=utf-8
import time
from random import randint
import base64
from os import path
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
    name = get_random_string(32) + '.png'
    pyplot.savefig(directory + name, dpi=300)
    return name


def plot_tree(g, root):
    pyplot.cla()
    pyplot.clf()
    pos = graphviz_layout(nx.bfs_tree(g, root), prog='dot', root=root)
    nx.draw_networkx_edges(g, pos)
    nxnodes = nx.draw_networkx_nodes(g, pos, node_color="w")
    nxnodes.set_edgecolor('k')
    nx.draw_networkx_labels(g, pos, font_color="k", font_size=8)
    pyplot.axis('off')
    return save_tree()


if __name__ == '__main__':
    with timer():
        time.sleep(1)
