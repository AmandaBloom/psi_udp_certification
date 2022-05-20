import socket
from urllib import response

PORT = 5053
SERVER = "172.16.14.44"
ADDR = (SERVER, PORT)
HEADER_SIZE = 128
ENCODING_TYPE = 'utf-8'
# ENCODING_TYPE = 'ascii'
DISCONNECT_MSG = "/EOF"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send_m(msg):
    msg = msg.encode(ENCODING_TYPE)
    client.sendall(msg) 
    print(client.recv(2048).decode(ENCODING_TYPE))

send_m("Hello1")
input()
send_m("Hello2")
input()
send_m(DISCONNECT_MSG)

