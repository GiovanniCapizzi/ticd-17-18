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


def SturmGen(Dn, MAX_R):
    d_list = [randint(0, MAX_R)] + [randint(1, MAX_R) for i in range(Dn)]

    S0 = '0'
    S1 = '1'

    for i in range(len(S1), Dn + 1):
        S0, S1 = S1, S1 * d_list[i] + S0
    return S1


if __name__ == '__main__':
    SturmGen(5, 5)
    with timer():
        time.sleep(1)
