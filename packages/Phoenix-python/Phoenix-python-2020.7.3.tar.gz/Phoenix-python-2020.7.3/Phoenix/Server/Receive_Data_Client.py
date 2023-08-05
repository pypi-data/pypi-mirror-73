import socket
import os
import threading
import time
import requests
from pathlib import Path


def Connect_Server(port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", port))
    return Receive_Server(client_socket)

def ReceiveData():
    home = str(Path.home())
    # print(self.home)
    ft = home + "\\PhoenixSettings\\Connection"
    my_file = Path(ft + ".pxc")
    if my_file.is_file():
        file = open(ft + ".pxc", "r", encoding="utf-8")
        data = file.read()
        data = data + "0"
        print(data)
        port = int(data)
        print(type(port))
        Connect_Server(port)
        file.close()

def ReceiveData(port):
    return Connect_Server(port)

def Receive_Server(client_socket):
    length_of_message = int.from_bytes(client_socket.recv(2), byteorder='big')
    data = client_socket.recv(length_of_message)
    data = data.decode('utf-8')
    return data
    #print("Received Response From Server......(" + data + ")")

#print(ReceiveData(55000))