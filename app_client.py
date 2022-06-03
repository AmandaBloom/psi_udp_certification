from copyreg import pickle
import pickle
from pydoc import cli
import time
from client import Client
from message import Message
from stream import Stream
import sys
import sys
import time
from urllib import response
import threading

ENCODING_TYPE = 'utf-8'
PORT = 5053
HEADER_SIZE = 128
DISCONECT = ""

class AppClient:
    def __init__(self, port, header_size, server_adr, ip_protocol):
        self.port = port
        self.header_size = header_size
        self.server_adr = server_adr
        self.ip_protocol = ip_protocol
        self.ever_clients = 0
        self.ever_streams = 0
        self.clients = []       
        self.streams = [] 

    # def __str__(self):
    #     return f"clients: \n {str(self.clients)} \n streams: \n {str(self.streams)} \n"

    def get_messages1(self, num, stream_id, con_id):
        messages = []
        for i in range(1, num + 1):
            m = Message(i, stream_id, con_id, f"witam serdecznie {i} {stream_id} {con_id}")
            messages.append(m)
            time.sleep(0.2)
        
        return messages
    
    def add_client(self):
        self.ever_clients += 1
        client_id = self.ever_clients
        client = Client(client_id, self.port, self.header_size, self.server_adr, self.ip_protocol)
        self.clients.append(client)
        self.connect_client(client_id)

    def get_client(self, client_id):
        for client in self.clients:
            if client.client_id == client_id:
                return client
        
        return False

    def get_clients(self):
        return self.clients

    def connect_client(self, client_id):
        client = self.get_client(client_id)
        if client:
            client.connect()
        else:
            print(f"client {client.client_id} not exists")

    def disconnect_client(self, client_id):
        client = self.get_client(client_id)
        if client:
            client.disconnect()
        else:
            print(f"client {client.client_id} not exists")

    def get_clients_ids(self):
        ids = []
        for client in self.clients:
            ids.append(client.client_id)
        
        return ids

    def get_streams_ids(self):
        ids = []
        for stream in self.streams:
            ids.append(stream.stream_id)
        
        return ids
    
    def disconnect_clients(self):
        ids = self.get_clients_ids()
        for client_id in ids:
            self.disconnect_client(client_id)

    # stream
    # stream_id, con_id
    
        
    def add_stream(self, client_id):
        self.ever_streams += 1
        stream_id = self.ever_streams
        stream = Stream(stream_id, client_id)
        self.streams.append(stream)

    def get_stream(self, stream_id):
        for stream in self.streams:
            if stream.stream_id == stream_id:
                return stream
        return False

    def send_stream(self, client_id, stream_id):
        client = self.get_client(client_id)
        stream = self.get_stream(stream_id)
        # stream.load_stream(self.get_messages1(10, stream_id, client_id))
        msg_stream = pickle.dumps(stream)
        client.send_m(msg_stream)

    def get_client_streams(self, client_id):
        ids = []
        for stream in self.streams:
            if stream.con_id == client_id:
                ids.append(stream.stream_id)
        return ids

    def send_streams(self, client_id):
        ids = self.get_client_streams(client_id)
        for id in ids:
            self.send_stream(client_id, id)
        
    def delete_stream(self):
        pass


def run_app_client(port, header_size, server_adr, ip_protocol):
    print("Welcome to AppClient")
    print("Working...")
    app = AppClient(port, header_size, server_adr, ip_protocol)
    app.add_client()
    app.add_client()

    app.add_stream(1)
    app.add_stream(1)
    app.add_stream(1)
    app.add_stream(2)
    app.add_stream(2)

    client_ids = app.get_clients_ids()

    # load sample data to streams concurently 
    waiting = []

    for client_id in client_ids:
        for stream_id in app.get_client_streams(client_id):
            stream = app.get_stream(stream_id)
            # stream.load_stream(app.get_messages1(10, stream_id, client_id))
            t = threading.Thread(target=stream.load_stream, args=[app.get_messages1(10, stream_id, client_id)])
            t.start()
            waiting.append(t)

    for t in waiting:
        t.join()

    s1 = threading.Thread(target=app.send_streams, args=[1])
    s2 = threading.Thread(target=app.send_streams, args=[2])
    s1.start()
    s2.start()
    s1.join()
    s2.join()

    app.disconnect_clients()


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
        run_app_client(port=PORT, header_size=HEADER_SIZE, server_adr=server_adr, ip_protocol=ip_protocol)
