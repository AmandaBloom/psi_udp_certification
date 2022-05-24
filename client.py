import csv
import socket
import sys
import time
from urllib import response

HEADER_SIZE = 1000
PORT = 5053
SERVER_IPV4 = "127.0.1.1"
SERVER_IPV6 = "::1"

ENCODING_TYPE = 'utf-8'
# ENCODING_TYPE = 'ascii'
DISCONNECT_MSG = "/EOF"


def send_m(msg):
    msg = msg.encode(ENCODING_TYPE)
    client.sendall(msg)
    print(client.recv(2048).decode(ENCODING_TYPE),end='\n')


if __name__ == "__main__":
    try:
        if sys.argv[1] == "v4":
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # ipv4
            ADDR = (SERVER_IPV4, PORT)
        elif sys.argv[1] == "v6":
            client = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)  # ipv4
            ADDR = (SERVER_IPV6, PORT)
    except IndexError:
        print("Provide correct IP protocol: v4 or v6")
        sys.exit(0)

    client.connect(ADDR)

    with open('sampleCSV/ford_escort.csv', 'r', encoding=ENCODING_TYPE) as file:
        msg = file.read()
        send_m(msg)

    time.sleep(1)

    with open('sampleCSV/trees.csv', 'r', encoding=ENCODING_TYPE) as file:
        msg = file.read()
        send_m(msg)

    time.sleep(1)

    send_m(DISCONNECT_MSG)
