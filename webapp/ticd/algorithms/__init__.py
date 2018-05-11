# coding=utf-8
import importlib
from os import listdir, path

from . import unary_coding

excluded = ['compiled_libraries', 'utils.py', 'divina_commedia.txt', 'pytest.ini', 'test_file.py', '.pytest_cache', 'Eratosthenes.py']

files = [file for file in listdir(path.dirname(__file__)) if '__' not in file and file not in excluded]

modules = {file[:-3]: importlib.import_module('.' + file[:-3], package='ticd.algorithms') for file in files}

algs = [(module.__algorithm__ if hasattr(module, '__algorithm__') else name, name) for name, module in modules.items()]
