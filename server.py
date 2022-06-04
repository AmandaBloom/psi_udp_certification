from asyncio import wait_for
import csv
from sys import platform
import socket
import threading
from concurrent.futures import thread
from datetime import datetime
from handlers import deserialize, save_stream
import ssl

class Server:
    def __init__(self, port, header_size, ip_protocol, server_adr=None, encoding='utf-8', disconnect_msg="disconnect"):
        self.port = port
        self.header_size = header_size
        self.encoding = encoding 
        self.disconnect_msg = disconnect_msg
        self.server_cert = 'server_certs/server.crt'
        self.server_key = 'server_certs/server.key'
        self.client_certs = 'client_certs/client.crt'
        self.interrupt_flag = 0
        self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.context.verify_mode = ssl.CERT_REQUIRED

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

    def new_client(self, val, addr, conn_with_client):
        print(f"New Client --- {self.server_adr}:{addr[1]} connected")
        connected = True
        while connected:
            msg_len = conn_with_client.recv(self.header_size).decode(self.encoding)
            if msg_len:
                msg_len = int(msg_len)
                msg = conn_with_client.recv(msg_len)

            if msg == str.encode(self.disconnect_msg):
                connected = False
                print(f"from: {self.server_adr}:{addr[1]} disconnect message")
            else:
                print(f"from: {self.server_adr}:{addr[1]} message_len: {len(msg)}")

                received_stream = deserialize(msg)
                save_stream(received_stream, display=False)
                response = "Recived stream nr " + str(len(msg)) + " " + str(datetime.now().strftime("%m_%d_%Y_%H:%M:%S"))
                conn_with_client.sendall(response.encode(self.encoding))
        print("client disconected")
        conn_with_client.close()
    
    def start(self):
        print(f"Server is listening... {self.server_adr}:{self.port}")
        self.server.listen()
        while True:
            try:
                val, addr = self.server.accept()
                self.context.load_cert_chain(certfile=self.server_cert, keyfile=self.server_key)
                self.context.load_verify_locations(cafile=self.client_certs)
                conn_with_client = self.context.wrap_socket(val, server_side=True)
                print("SSL established. Peer: {}".format(conn_with_client.getpeercert()))
                new_thread = threading.Thread(target=self.new_client, args=(val, addr, conn_with_client))
                new_thread.start()
                print(f"connected clients: {threading.active_count() - 1}")
            except ssl.SSLError as ssl_error:
                print(ssl_error)
                print("Client: " + str(addr[1]) + " has no SSL and won't be connected to the server")
                self.start()
            except KeyboardInterrupt:
                self.server.close()
                print("\nKeyboard Interrupt")
                print("Connection closed.\nSession ended.")
                return


