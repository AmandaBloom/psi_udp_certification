from asyncio import wait_for
import csv
from sys import platform
import socket
import threading
from concurrent.futures import thread
from datetime import datetime
from handlers import deserialize, save_stream

class Server:
    def __init__(self, port, header_size, ip_protocol, server_adr=None, encoding='utf-8', disconnect_msg=""):
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
                if platform == "win32":
                    self.server_adr = socket.gethostbyname(socket.gethostname()+".local")
                elif platform == "linux" or platform == "linux2":
                    self.server_adr = socket.gethostbyname(socket.gethostname())
                print(self.server_adr)
            else:
                self.server_adr = server_adr   
            self.addr = (self.server_adr, self.port)
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # ipv4
            self.server.bind(self.addr)

    def new_client(self, val, addr):
        print(f"New Client --- {self.server_adr}:{addr[1]} connected")
        connected = True
        while connected:
            msg_len = val.recv(self.header_size).decode(self.encoding)
            print("msg_len", msg_len)
            if msg_len:
                if int(msg_len) == len(self.disconnect_msg):
                    connected = False
                else:
                    msg_len = int(msg_len)
                    msg = val.recv(msg_len)
                    print(f"from: {self.server_adr}:{addr[1]} message_len: {len(msg)}")

                    received_stream = deserialize(msg)
                    save_stream(received_stream, display=True)
                    response = "Recived stream nr " + str(len(msg)) + " " + str(datetime.now().strftime("%m_%d_%Y_%H:%M:%S"))
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
                self.server.close()
                print("\nKeyboard Interrupt")
                print("Connection closed.\nSession ended.")
                return

            new_thread = threading.Thread(target=self.new_client, args=(val, addr))
            new_thread.start()
            print(f"connected clients: {threading.active_count() - 1}")
