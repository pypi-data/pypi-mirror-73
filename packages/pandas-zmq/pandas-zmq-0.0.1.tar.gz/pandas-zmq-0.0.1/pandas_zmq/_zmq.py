
import zlib
import pickle
from zmq import *


def send_dataframe(socket, obj, flags=0):
    """send pandas dataframe***"""
    p = pickle.dumps(obj, -1)
    z = zlib.compress(p)
    return socket.send(z, flags=flags)


def recv_dataframe(socket, flags=0):
    """receive pandas dataframe***"""
    z = socket.recv(flags)
    p = zlib.decompress(z)
    return pickle.loads(p)
