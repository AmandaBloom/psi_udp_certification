from copyreg import pickle
import pickle
import time
from client import Client
from message import Message
from stream import Stream
import sys
import csv
import socket
import sys
import time
from urllib import response

ENCODING_TYPE = 'utf-8'
PORT = 5053
HEADER_SIZE = 128
DISCONECT = ""

def app_client(encoding_type, port, header_size, server_adr, ip_protocol):
    c1 = Client(port=port, header_size=header_size, server_adr=server_adr, ip_protocol=ip_protocol)
    c1.connect()
    s1 = Stream(1, 1)
    s2 = Stream(2, 2)
    m1 = Message(1, 1, 1, "witam serdecznie1")
    m2 = Message(2, 1, 1, "witam serdecznie2")
    m3 = Message(3, 1, 1, "witam serdecznie3")
    m4 = Message(4, 1, 1, "witam serdecznie4")
    m5 = Message(5, 2, 2, "witam serdecznie5")
    m6 = Message(6, 2, 2, "witam serdecznie6")
    s1.add_message(m1)
    s1.add_message(m2)
    s1.add_message(m3)
    s1.add_message(m4)
    s2.add_message(m5)
    s2.add_message(m6)

    msg = pickle.dumps(s1)
    c1.send_m(msg)
    msg = pickle.dumps(s2)
    c1.send_m(msg)
    print(DISCONECT.encode(ENCODING_TYPE))
    time.sleep(1)
    c1.disconnect()


if __name__ == "__main__":
    ip_protocol = None
    server_adr = None
    # ip_protocol = "v4"
    # server_adr = "127.0.0.1"
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
