# coding=utf-8
from math import log
from collections import deque  # https://docs.python.org/2/library/collections.html#collections.deque

values = [3, 53, 64, 73, 42, 128]


# PEP8


def encode(val): return '0' * int(log(val, 2)) + "{0:b}".format(val)


def decode(bin_str):
    queue = deque(bin_str)
    output = []
    N = 0
    while len(queue):
        bit = queue.popleft()
        if bit is '0':
            N += 1
        else:
            # Per avere N + 1
            temp = '1'
            while N:
                temp += queue.popleft()
                N -= 1
            output.append(int(temp, 2))
    return output


# TEST CODE ------------------
if __name__ == '__main__':
    toDecode = ""
    for v in values:
        print(encode(v))
        toDecode += encode(v)

    print("DECODING:", toDecode)

    print(decode(toDecode))
