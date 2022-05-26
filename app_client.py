import time
from client import Client
import sys
import csv
import socket
import sys
import time
from urllib import response

ENCODING_TYPE = 'utf-8'
PORT = 5053
HEADER_SIZE = 1024
SERVER_IPV4 = "172.16.14.44"
SERVER_IPV6 = "::1"

def app_client(encoding_type, port, header_size, server_adr, ip_protocol):
    c1 = Client(port=port, header_size=header_size, server_adr=server_adr, ip_protocol=ip_protocol)
    c1.connect()
    c1.send_m('hello hello hello')
    time.sleep(1)

    with open('sampleCSV/ford_escort.csv', 'r', encoding=encoding_type) as file:
        msg = file.read()
        c1.send_m(msg)
    time.sleep(1)

    with open('sampleCSV/trees.csv', 'r', encoding=encoding_type) as file:
        msg = file.read()
        c1.send_m(msg)
    time.sleep(1)

    c1.disconnect()

if __name__ == "__main__":
    ip_protocol = None
    server_adr = None
    try:
        if sys.argv[1] == "v4":
            ip_protocol = "v4"
            server_adr = SERVER_IPV4
        elif sys.argv[1] == "v6":
            ip_protocol = "v6"
            server_adr = SERVER_IPV6
    except IndexError:
        print("Provide correct IP protocol: v4 or v6")
        sys.exit(0)
    if ip_protocol and server_adr:
        app_client(encoding_type=ENCODING_TYPE, port=PORT, header_size=HEADER_SIZE, server_adr=server_adr, ip_protocol=ip_protocol)

