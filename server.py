from concurrent.futures import thread
import socket
import threading

HEADER_SIZE = 128
PORT = 5053
SERVER = socket.gethostbyname(socket.gethostname()+".local")
ADDR = (SERVER, PORT)
ENCODING_TYPE = 'utf-8'
# ENCODING_TYPE = 'ascii'
DISCONNECT_MSG = "/EOF"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # ipv4
server.bind(ADDR) 

def new_client(val, addr):
    print(f"{addr} connected")
    connected = True
    while connected:
        msg = val.recv(HEADER_SIZE).decode(ENCODING_TYPE)
        print("from: ", addr, " message: ", msg)
        response = "Recived msg " + str(len(msg))
        if msg == DISCONNECT_MSG:
            connected = False
        val.sendall(response.encode(ENCODING_TYPE))
    print("client disconected")
    val.close()

def start():
    print(f"Server is listening...")
    server.listen()
    while True:
        val, addr = server.accept()
        thread = threading.Thread(target=new_client, args=(val, addr))
        thread.start()
        print(f"connected clients: {threading.active_count() - 1}")
    

start()
