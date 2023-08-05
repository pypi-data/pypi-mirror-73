from base64 import *
from string import printable
from itertools import permutations

key = {}
per = list(permutations(printable, 2))
per = [''.join(x) for x in per]

for x in printable:
    per.append(x*2)

y = 127
for x in per:
    key[x] = chr(y)
    y += 1

def compress(bytes_data):
    data = b64encode(bytes_data).decode()
    for x, y in key.items():
        data = data.replace(x, y)
    return data

def decompress(string_data):
    data = string_data
    for x, y in key.items():
        data = data.replace(y, x)
    return b64decode(data.encode())
