import csv
import socket
import sys
import time
from urllib import response
import ssl

class Client:
    def __init__(self, port, header_size, server_adr, ip_protocol, encoding='utf-8', disconnect_msg="/EOF"):
        self.port = port
        self.header_size = header_size
        self.server_adr = server_adr
        self.encoding = encoding
        self.addr = (self.server_adr, self.port)
        self.disconnect_msg = disconnect_msg
        self.server_sni_hostname = 'PSI'
        self.server_cert = 'server.crt'
        self.client_cert = 'client.crt'
        self.client_key = 'client.key'
        self.context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=self.server_cert)
        self.context.load_cert_chain(certfile=self.client_cert, keyfile=self.client_key)
        if ip_protocol == "v6":
            self.client = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        else:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.conn = self.context.wrap_socket(self.client, server_side=False, server_hostname=self.server_sni_hostname)
        self.conn.connect(self.addr)
        print("SSL established. Peer: {}".format(self.conn.getpeercert()))

    def disconnect(self):
        msg = self.disconnect_msg.encode(self.encoding)
        msg_len = len(msg)
        send_len = str(msg_len).encode(self.encoding)
        send_len += b' ' * (self.header_size - len(send_len)) 
        self.conn.send(send_len)
        self.conn.send(msg) 
        
    def send_m(self, msg):
        msg = msg.encode(self.encoding)
        msg_len = len(msg)
        send_len = str(msg_len).encode(self.encoding)
        send_len += b' ' * (self.header_size - len(send_len)) 
        self.conn.send(send_len)
        self.conn.send(msg) 
        print(self.conn.recv(2048).decode(self.encoding))


 
