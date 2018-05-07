from .bwt import encode
from .utils import timer

data = ""

with open('divina_commedia.txt') as file:
    lines = file.readlines()
    for line in lines:
        print(encode(line, True))
