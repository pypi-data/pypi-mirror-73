__version__ = '0.1.7'
__author__ = 'Sandra Mattar'
__email__ = 'sandrawmattar@gmail.com'
__url__ = 'https://pypi.org/project/compresspy'

from base64 import *
import pickle
import os

key = pickle.loads(b64decode(open(os.path.join(os.path.dirname(__file__),
                                               'key.dat'),
                                  'r').read().encode()))

def compress(bytes_data):
    data = b64encode(bytes_data).decode()
    for x, y in key.items():
        data = data.replace(x, y)
    return data

def compressobj(obj):
    return compress(pickle.dumps(obj))

def decompress(string_data):
    data = string_data
    for x, y in key.items():
        data = data.replace(y, x)
    return b64decode(data.encode())

def decompressobj(string_data):
    return pickle.loads(decompress(string_data))
