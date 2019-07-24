import socket
import threading
from time import sleep


class sysClient(threading.Thread):
    def __init__(self, address, port, message, sock=None):
        super().__init__()
        self.address = address
        self.port = port
        self.message = message
        if sock is None:
            self.sock = socket.socket()
        else:
            self.sock = sock

    def run(self):
        self.sock.connect((self.address, self.port))
        self.sock.sendall(self.message.encode("ascii"))
        sleep(1)
        self.sock.close()


class sysServer(threading.Thread):
    def __init__(self, address, port, sock=None):
        super().__init__()
        self.address = address
        self.port = port
        if sock is None:
            self.sock = socket.socket()
        else:
            self.sock = sock

    def run(self):
        self.sock.bind((self.address, self.port))
        self.sock.listen(1)
        print(self.awaitConnection())

    def awaitConnection(self):
        while True:
            connection, client_address = self.sock.accept()
            try:
                final = b""
                while True:
                    partial = connection.recv(16)
                    if partial:
                        final += partial
                    else:
                        print(final.decode("ascii"))
                        break
            finally:
                connection.close()
                break
        self.sock.close()
        return "sock closed on server"


srv = sysServer("localhost", 9998)
cli = sysClient("localhost", 9998, "hello!")
srv.start()
cli.start()
