# -*- coding: utf-8 -*-

from gc import collect
from typing import List
from heapq import heappop, heappush
from networkx.drawing.nx_pydot import graphviz_layout
from matplotlib import pyplot
import networkx as nx
from timeit import default_timer

from .delta_coder import DeltaCoder
from .utils import save_tree, plot_tree
from .utils import input_example

__algorithm__ = 'FGK'
__group__ = "miscellaneous"


class Node(object):
    def __init__(self, parent=None, left=None, right=None, weight=0, N=0, symbol=''):
        super(Node, self).__init__()
        self.parent = parent
        self.left = left
        self.right = right
        self.weight = weight
        self.N = N
        self.symbol = symbol

    def is_leaf(self):
        return self.left is None and self.right is None

    def is_left_child(self):
        return self.parent.left == self if self.parent is not None else False

    def is_right_child(self):
        return self.parent.right == self if self.parent is not None else False

    def __lt__(self, other):
        return self.N < other.N

    def __repr__(self):
        return str(self)

    def __str__(self):
        if self.N > 0:
            return f"{self.symbol} -> W: {self.weight}, N: {self.N}"
        else:
            return f"{self.symbol} -> W: {self.weight}"


class FGK(object):

    def __init__(self, alphabet_size):
        super(FGK, self).__init__()
        self.graph = nx.Graph()
        self.alphabet_size = alphabet_size
        self.__init_config()

    def __init_config(self):
        self.NYT = Node(symbol=b"NYT", weight=0, N=2 * self.alphabet_size + 1)
        self.root = self.NYT
        self.seen = {b"NYT": self.NYT}
        self.weights: Dict[int, List[Node]] = {0: [self.NYT]}
        self.distinct_symbols = 0
        self.total_symbols = 0

    def __get_code(self, s, node, code=''):
        if node is None:
            return ""
        if s.symbol == node.symbol:
            return code
        return self.__get_code(s, node.left, code=code + "0") + self.__get_code(s, node.right, code=code + "1")

    def __swap(self, a, b):
        # swap p and q
        a_right, b_right = a.is_right_child(), b.is_right_child()

        if a.parent:
            if a_right:
                a.parent.right = b
            else:
                a.parent.left = b

        if b.parent:
            if b_right:
                b.parent.right = a
            else:
                b.parent.left = a

        b.parent, a.parent = a.parent, b.parent
        b.N, a.N = a.N, b.N

    def __exchange(self, q, leaf=False):
        p = q

        # find node with same weight and max N
        for node in self.weights.get(q.weight, []):
            if leaf:
                if node.is_leaf() and p.N < node.N:
                    p = node
            else:
                if p.N < node.N:
                    p = node

        # swap p and q
        self.__swap(p, q)

        # remove q from weights queue
        if q in self.weights[q.weight]:
            self.weights[q.weight].remove(q)

        # increase weight of q and update list
        q.weight += 1
        self.weights[q.weight] = self.weights.get(q.weight, []) + [q]

        return q.parent

    def __is_nyt_sibling(self, x):
        return x.parent.left == self.NYT or x.parent.right == self.NYT

    def __create_new_node(self, symbol):
        node = Node(symbol=b"".join([b"NYT", symbol]))
        node.left, node.right = self.NYT, Node(symbol=symbol, weight=0)

        node.N = self.NYT.N
        node.right.N = self.NYT.N - 1
        self.NYT.N -= 2

        if self.NYT.parent is not None:
            node.parent = self.NYT.parent
            self.NYT.parent.left = node
            self.NYT.parent = node
        else:
            self.NYT.parent = node
            self.root = node

        node.left.parent, node.right.parent = node, node
        # node.weight = node.left.weight + node.right.weight

        self.seen[symbol] = node.right
        self.seen[node.symbol] = node  # needed only for plot
        self.weights[0] = self.weights.get(0, []) + [node.right, node]
        self.distinct_symbols += 1
        return node.right

    def __update(self, symbol):
        symbol_code = 0
        q = self.seen.get(symbol, None)

        # insert new node for symbol
        if q is None and self.distinct_symbols < self.total_symbols:
            q = self.__create_new_node(symbol)
            symbol_code = 257 + ord(symbol.decode("unicode-escape"))

        symbol_code = symbol_code if symbol_code != 0 else self.seen[
            symbol].N  # self.__get_code(self.seen[symbol], self.root)

        # exchanges leaves
        if self.__is_nyt_sibling(q):
            q = self.__exchange(q, leaf=True)

        # exchanges nodes
        while q is not None:
            q = self.__exchange(q, leaf=False)

        return symbol_code

    def __search(self, x, n):
        if x is None:
            return b""
        if x.N == n:
            return x.symbol
        return self.__search(x.left, n) + self.__search(x.right, n)

    # def __search(self, x, n):
    #     if x.is_leaf():
    #         return x.symbol
    #     if n[0] == "0":
    #         return self.__search(x.left, n[1:])
    #     elif n[0] == "1":
    #         return self.__search(x.right, n[1:])

    def __build_graph(self, x):
        if x is None:
            return
        if x.left is not None:
            self.graph.add_edge(x.symbol, x.left.symbol)
        if x.right is not None:
            self.graph.add_edge(x.symbol, x.right.symbol)
        self.__build_graph(x.left)
        self.__build_graph(x.right)

    def plot(self, text):
        pyplot.cla()
        pyplot.clf()

        cast = lambda x: x.decode("unicode-escape").encode("utf8").decode("utf8", "backslashreplace")

        text = [c.encode("unicode-escape") for c in set(text)]
        source = self.root.symbol
        self.__build_graph(self.root)

        pos = graphviz_layout(nx.bfs_tree(self.graph, source), prog='dot', root=source)
        edge_labels = dict([((u, v,), "0" if self.seen[v].is_left_child() else "1") for u, v in self.graph.edges()])
        # node_labels = dict([(v, cast((v if v in text or v == b"NYT" else b" ") + b" W: {}, N: {}".format(self.seen[v].weight, self.seen[v].N))) for v in self.graph.nodes()])
        node_labels = dict([(v, cast(v if v in text or v == b"NYT" else b"")) for v in self.graph.nodes()])
        node_sizes = [len(v) * 150 if len(v) > 0 else 40 for _, v in node_labels.items()]
        nx.draw_networkx_edges(self.graph, pos)
        nxnodes = nx.draw_networkx_nodes(self.graph, pos, node_size=node_sizes, node_color="w")
        nxnodes.set_edgecolor('k')
        nx.draw_networkx_edge_labels(self.graph, pos, font_size=8, edge_labels=edge_labels)
        nx.draw_networkx_labels(self.graph, pos, font_color="k", font_size=8, labels=node_labels)

        pyplot.axis('off')
        # pyplot.show()
        # self.graph.clear()
        return save_tree()

    def __del_graph(self, x):
        if x is None:
            return
        self.__del_graph(x.left)
        self.__del_graph(x.right)
        del x.left, x.right, x.parent, x

    def __clear_config(self):
        del self.weights, self.seen
        self.__del_graph(self.root)
        collect()
        self.__init_config()
        self.graph.clear()

    def encode(self, text, plot=False):
        self.total_symbols = len(text)
        result = []
        for s in text:
            result.append(self.__update(s.encode("unicode-escape")))
        return result

    def decode(self, sequence):
        self.total_symbols = len(sequence)
        result = b""
        for s in sequence:
            if s >= 257:
                tmp = chr(s - 257).encode("unicode-escape")
                result += tmp
                self.__update(tmp)
            else:
                tmp = self.__search(self.root, s)
                result += tmp
                self.__update(tmp)
            # if type(s) != str:
            #    tmp = chr(s - 257).encode("unicode-escape")
            #    result += tmp
            #    self.__update(tmp)
            # else:
            #     tmp = self.__search(self.root, s)
            #     result += tmp if tmp is not None else ""
            #     if tmp is not None:
            #         self.__update(tmp)
        self.__clear_config()
        return result.decode("unicode-escape")


@input_example(text="we have the best prof ever")
def encode(text: str):
    fgk = FGK(len(set(text)))
    return {
        'sequence': DeltaCoder().encode_sequence(fgk.encode(text)),
        'number_of_symbols': len(set(text)),
        'edges': fgk.plot(text)
    }


@input_example(number_of_symbols="13 symbols for \"we have the best prof ever\"", sequence="00010010111100000010010110011000010010010000100010010110100100010010110001000010...")
def decode(number_of_symbols: int, sequence: str):
    return FGK(number_of_symbols).decode(DeltaCoder().decode_text(sequence))


def test(word, plot=False):
    start = default_timer()
    fgk = FGK(len(set(word)))
    enc = fgk.encode(word, plot)
    print("Encoding time -> {}".format(default_timer() - start))
    start = default_timer()
    dec = fgk.decode(enc)
    print("Decoding time -> {}".format(default_timer() - start))
    assert word == dec

# if __name__ == '__main__':
#    Fire()
