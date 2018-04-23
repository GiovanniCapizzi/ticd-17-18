# coding=utf-8
import time


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


if __name__ == '__main__':
    with timer():
        time.sleep(1)
