from asyncio import wait_for
import csv
from sys import platform
import socket
import threading
from concurrent.futures import thread
from datetime import datetime
import ssl

class Server:
    def __init__(self, port, header_size, ip_protocol, server_adr=None, encoding='utf-8', disconnect_msg="/EOF"):
        self.port = port
        self.header_size = header_size
        self.encoding = encoding 
        self.disconnect_msg = disconnect_msg
        self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.context.verify_mode = ssl.CERT_REQUIRED
        self.server_cert = 'server.crt'
        self.server_key = 'server.key'
        self.client_certs = 'client.crt'
        self.interrupt_flag = 0

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

    def new_client(self, val, addr, conn_with_client, connected):
        print(f"New Client --- {self.server_adr}:{addr[1]} connected")
        
        while connected:
            try:
                msg_len = conn_with_client.recv(self.header_size).decode(self.encoding)
            except ConnectionResetError:
                msg_len = 0
            except OSError:
                msg_len = 0
            if msg_len:
                msg_len = int(msg_len)
                msg = conn_with_client.recv(msg_len).decode(self.encoding)
                print(f"from: {self.server_adr}:{addr[1]} message_len: {len(msg)}")

                if len(msg) > 5:
                    with open(
                        './recv/recv'+str(datetime.now().strftime("%m_%d_%Y_%H%M%S_"))+ str(addr[1]) + ".csv", 'w'
                            ) as f:
                        f.write(msg)

                response = "Recived msg " + str(len(msg)) + " " + str(datetime.now().strftime("%m_%d_%Y_%H:%M:%S"))
                if msg == self.disconnect_msg:
                    connected = False
                conn_with_client.sendall(response.encode(self.encoding))
 
        print("client disconected")
        conn_with_client.close()
    
    def start(self):
        print(f"Server is listening... {self.server_adr}:{self.port}")
        self.server.listen()
        while self.interrupt_flag != 1:
            connected = True
            try:
                val, addr = self.server.accept()
                self.context.load_cert_chain(certfile=self.server_cert, keyfile=self.server_key)
                self.context.load_verify_locations(cafile=self.client_certs)
                conn_with_client = self.context.wrap_socket(val, server_side=True)
                print("SSL established. Peer: {}".format(conn_with_client.getpeercert()))

            except ssl.SSLError as ssl_error:
                print(ssl_error)
                print("Client: " + str(addr[1]) + " has no SSL and won't be connected to the server")
                conn_with_client.close()
                self.start()
                
            except KeyboardInterrupt:
                self.interrupt_flag = 1
                self.server.close()
                print("\nKeyboard Interrupt")
                print("Connection closed.\nSession ended.")
                connected=False
                return
            
            if(self.interrupt_flag != 1):
                new_thread = threading.Thread(target=self.new_client, args=(val, addr, conn_with_client, connected))
                new_thread.start()
                print(f"connected clients: {threading.active_count() - 1}")
