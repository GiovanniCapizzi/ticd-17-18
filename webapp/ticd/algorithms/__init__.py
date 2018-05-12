# coding=utf-8
import importlib
from os import listdir, path

from . import unary_coding

excluded = open(path.dirname(__file__) + '/.algorithmsignore', 'r').read().split('\n')

files = [file for file in listdir(path.dirname(__file__)) if '__' not in file and file not in excluded]

modules = {file[:-3]: importlib.import_module('.' + file[:-3], package='ticd.algorithms') for file in files}

algs = {module.__group__: [] for name, module in modules.items()}

for name, module in modules.items():
    algs[module.__group__].append((module.__algorithm__ if hasattr(module, '__algorithm__') else name, name))

algs = {name: sorted(value, key=lambda x: x[0]) for name, value in algs.items()}
