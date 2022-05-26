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
                    './recv/recv:'+str(datetime.now().strftime("%m_%d_%Y_%H:%M:%S"))+".csv", 'w'
                        ) as f:
                    f.write(msg)

            response = "Recived msg " + str(len(msg)) + " " + str(datetime.now().strftime("%m_%d_%Y_%H:%M:%S"))
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
