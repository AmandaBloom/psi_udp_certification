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
