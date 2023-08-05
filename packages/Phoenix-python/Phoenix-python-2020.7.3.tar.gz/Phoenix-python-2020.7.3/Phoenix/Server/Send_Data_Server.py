import socket
import os
import threading
import time
import requests
from pathlib import Path


def Connect_Server(port, Msg):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", port))
    server_socket.listen(5)
    return Send_Server(server_socket, Msg)

def SendData(Msg):
    sent=False
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
        sent=Connect_Server(port,Msg)
        file.close()
    return sent

def SendData(port,Msg):
    return Connect_Server(port,Msg)

def Send_Server(server_socket,Msg):
    conn, addr = server_socket.accept()
    #print("Got connection from", addr)
    sent=False
    data=Msg+"\nno more data"
    conn.send(str.encode(data))
    sent=True
    if("Close Connection" in data):
        #print("Closing Connection......")
        data = "Closing Connection"
        server_socket.close()

    elif("Close Client" in data):
        #print("Closing Client......")
        data = "Closing Client"
        #print("Closed Client......")
        server_socket.close()

    else:
        #print("Sending Response To Server......("+Msg+")")
        #print("Send Response To Server......("+Msg+")")
        server_socket.close()
    return sent

#print(SendData(55000,"#ivona"))