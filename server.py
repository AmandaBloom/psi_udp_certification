<<<<<<< HEAD
import csv
import socket
import sys
import threading
from concurrent.futures import thread
from datetime import datetime

HEADER_SIZE = 1000
PORT = 5053
SERVER_IPV4 = socket.gethostbyname(socket.gethostname())
SERVER_V6 = socket.getaddrinfo("localhost", port=PORT, family=socket.AF_INET6)
SERVER_IPV6 = SERVER_V6[0][4][0]

ENCODING_TYPE = 'utf-8'
# ENCODING_TYPE = 'ascii'
DISCONNECT_MSG = "/EOF"


def new_client(val, addr):
    print(f"{addr} connected")
    connected = True
    while connected:
        msg = val.recv(HEADER_SIZE).decode(ENCODING_TYPE)
        print("from: ", addr, " message_len: ", len(msg))

        if len(msg) > 5:
            with open(
                './recv/recv'+str(datetime.timestamp(datetime.now()))+".csv", 'w'
                    ) as f:
                f.write(msg)

        response = "Recived msg " + str(len(msg))
        if msg == DISCONNECT_MSG:
            connected = False
        val.sendall(response.encode(ENCODING_TYPE))
    print("client disconected")
    val.close()


def start(socket, serverAddress):
    socket.listen(5)
    print(
        f"Server is listening on... {serverAddress[0]}:{str(serverAddress[1])}"
        )
    while True:
        try:
            val, addr = socket.accept()
        except KeyboardInterrupt:
            socket.close()
            print("\nKeyboard Interrupt")
            print("Connection closed.\nSession ended.")
            return

        new_thread = threading.Thread(target=new_client, args=(val, addr))
        new_thread.start()
        print(f"connected clients: {threading.active_count() - 1}")


if __name__ == "__main__":
    try:
        if sys.argv[1] == "v4":
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # ipv4
            ADDR = (SERVER_IPV4, PORT)
        elif sys.argv[1] == "v6":
            server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)  # ipv4
            ADDR = (SERVER_IPV6, PORT)
    except IndexError:
        print("Provide correct IP protocol: v4 or v6")
        sys.exit(0)

    server.bind(ADDR)

    start(server, ADDR)
=======
import csv
import socket
import threading
from concurrent.futures import thread
from datetime import datetime

class Server:
    def __init__(self, port, header_size, ip_protocol, server_adr=None, encoding='utf-8', disconnect_msg="/EOF"):
        self.port = port
        self.header_size = header_size
        self.encoding = encoding 
        self.disconnect_msg = disconnect_msg
        if ip_protocol == "v6":
            if not server_adr:
                server_v6 = socket.getaddrinfo("localhost", port=port, family=socket.AF_INET6)
                self.server_adr = server_v6[0][4][0]
            else:
                self.server_adr = server_adr  
            self.addr = (self.server_adr, self.port)
            self.server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)  # ipv6
            self.server.bind(self.addr) 
        else:
            if not server_adr:
                self.server_adr = socket.gethostbyname(socket.gethostname()+".local")
            else:
                self.server_adr = server_adr   
            self.addr = (self.server_adr, self.port)
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # ipv4
            self.server.bind(self.addr) 

    def new_client(self, val, addr):
        print(f"{addr} connected")
        connected = True
        while connected:
            msg = val.recv(self.header_size).decode(self.encoding)
            print("from: ", addr, " message_len: ", len(msg))

            if len(msg) > 5:
                with open(
                    './recv/recv'+str(datetime.timestamp(datetime.now()))+".csv", 'w'
                        ) as f:
                    f.write(msg)

            response = "Recived msg " + str(len(msg))
            if msg == self.disconnect_msg:
                connected = False
            val.sendall(response.encode(self.encoding))
        print("client disconected")
        val.close()
    
    def start(self):
        print(f"Server is listening... {self.server_adr}:{self.port}")
        self.server.listen()
        while True:
            try:
                val, addr = self.server.accept()
            except KeyboardInterrupt:
                socket.close()
                print("\nKeyboard Interrupt")
                print("Connection closed.\nSession ended.")
                return
            
            new_thread = threading.Thread(target=self.new_client, args=(val, addr))
            new_thread.start()
            print(f"connected clients: {threading.active_count() - 1}")
>>>>>>> dev
