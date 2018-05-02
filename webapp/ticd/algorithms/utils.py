# coding=utf-8
import time
from random import randint


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


if __name__ == '__main__':
    with timer():
        time.sleep(1)
