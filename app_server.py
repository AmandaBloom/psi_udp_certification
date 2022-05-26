from server import Server
import sys

ENCODING_TYPE = 'utf-8'
PORT = 5053
HEADER_SIZE = 1024

def app_server(port, header_size, ip_protocol):
    s1 = Server(port=port, header_size=header_size, ip_protocol=ip_protocol)
    s1.start()

if __name__ == "__main__":
    ip_protocol = None
    try:
        if sys.argv[1] == "v4":
            ip_protocol = "v4"
        elif sys.argv[1] == "v6":
            ip_protocol = "v6"
    except IndexError:
        print("Provide correct IP protocol: v4 or v6")
        sys.exit(0)

    if ip_protocol:
        app_server(port=PORT, header_size=HEADER_SIZE, ip_protocol=ip_protocol)