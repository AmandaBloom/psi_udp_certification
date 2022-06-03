import time
from client import Client
from client_no_cert import Client_no_cert
import sys
import csv
import socket
import sys
import time
from urllib import response

ENCODING_TYPE = 'utf-8'
PORT = 5053
HEADER_SIZE = 128


def app_client(encoding_type, port, header_size, server_adr, ip_protocol):
    c1 = Client(port=port, header_size=header_size, server_adr=server_adr, ip_protocol=ip_protocol)
    c1.connect()
    time.sleep(1)

    with open('sampleCSV/ford_escort.csv', 'r', encoding=encoding_type) as file:
        msg = file.read()
        c1.send_m(msg)
    time.sleep(1)

    c2 = Client(port=port, header_size=header_size, server_adr=server_adr, ip_protocol=ip_protocol)
    c2.connect()
    with open('sampleCSV/trees.csv', 'r', encoding=encoding_type) as file:
        msg = file.read()
        c2.send_m(msg)
    time.sleep(1)
    c2.disconnect()
    with open('sampleCSV/trees.csv', 'r', encoding=encoding_type) as file:
        msg = file.read()
        c1.send_m(msg)
    time.sleep(1)

    c1.disconnect()
    c4 = Client_no_cert(port=port, header_size=header_size, server_adr=server_adr, ip_protocol=ip_protocol)
    c4.connect()
    c4.send_m('hello hello hello')
    c5 = Client(port=port, header_size=header_size, server_adr=server_adr, ip_protocol=ip_protocol)
    c5.connect()
    with open('sampleCSV/trees.csv', 'r', encoding=encoding_type) as file:
        msg = file.read()
        c5.send_m(msg)
    c5.disconnect()


if __name__ == "__main__":
    ip_protocol = None
    server_adr = None
    try:
        if sys.argv[2]:
            if sys.argv[1] == "v4":
                ip_protocol = "v4"
            elif sys.argv[1] == "v6":
                ip_protocol = "v6"
            server_adr = sys.argv[2]
    except IndexError:
        print("Provide correct IP protocol and server IP address (f.e /'v4 192.168.0.0/' or /'v6 ::32 /' ")
        sys.exit(0)

    if ip_protocol and server_adr:
        app_client(encoding_type=ENCODING_TYPE, port=PORT, header_size=HEADER_SIZE, server_adr=server_adr, ip_protocol=ip_protocol)
