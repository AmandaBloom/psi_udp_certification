import csv
import socket
import sys
import time
from urllib import response

class Client:
    def __init__(self, port, header_size, server_adr, ip_protocol, encoding='utf-8', disconnect_msg=""):
        self.port = port
        self.header_size = header_size
        self.server_adr = server_adr
        self.encoding = encoding
        self.addr = (self.server_adr, self.port)
        self.disconnect_msg = disconnect_msg
        if ip_protocol == "v6":
            self.client = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        else:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.client.connect(self.addr)

    def disconnect(self):
        self.send_m(self.disconnect_msg.encode())

    def send_m(self, msg):
        msg_len = len(msg)
        send_len = str(msg_len).encode(self.encoding)
        send_len += b' ' * (self.header_size - len(send_len)) 
        self.client.send(send_len)
        if isinstance(msg, str):
            msg = msg.encode()
        self.client.send(msg) 
        print(self.client.recv(1024).decode(self.encoding))


 
