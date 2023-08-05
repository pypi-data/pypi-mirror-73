import socket
import os
import threading
import time
import requests
from pathlib import Path

def Connect_Server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", port))
    server_socket.listen(5)
    return Receive_Server(server_socket)

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

def Receive_Server(server_socket):
    conn, addr = server_socket.accept()
    # print("Got connection from", addr)
    length_of_message = int.from_bytes(conn.recv(2), byteorder='big')
    data = conn.recv(length_of_message)
    data = data.decode('utf-8')
    return data

#print(ReceiveData(55001))