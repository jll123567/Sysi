import socket
import threading
from time import sleep


class sysClient(threading.Thread):
    def __init__(self, message, sAddress, sPort, rAddress, rPort, sSock=None, rSock=None, rStor=None, sStor=None):
        super().__init__()
        self.message = message
        self.sAddress = sAddress
        self.sPort = sPort
        self.rAddress = rAddress
        self.rPort = rPort
        self.rStor = rStor
        self.sStor = sStor
        if sSock is None:
            self.sSock = socket.socket()
        else:
            self.sSock = sSock
        if rSock is None:
            self.rSock = socket.socket()
        else:
            self.rSock = rSock

    def run(self):
        print(self.sendAscii(self.message))
        print(self.receiveAscii())

    def receiveAscii(self):
        self.rSock.bind((self.rAddress, self.rPort))
        self.rSock.listen(1)
        while True:
            connection, client_address = self.rSock.accept()
            final = b""
            try:
                while True:
                    partial = connection.recv(16)
                    if partial:
                        final += partial
                    else:
                        print(final.decode("ascii"))
                        break
            finally:
                self.rStor = final.decode("ascii")
                connection.close()
                break
        self.rSock.close()
        return "rSock closed on client"

    def sendAscii(self, msg):
        self.sSock.connect((self.sAddress, self.sPort))
        self.sSock.sendall(msg.encode("ascii"))
        sleep(5)
        self.sSock.close()
        return "sSock closed on client"


class sysServer(threading.Thread):
    def __init__(self, sAddress, sPort, rAddress, rPort, sSock=None, rSock=None, rStor=None, sStor=None):
        super().__init__()
        self.sAddress = sAddress
        self.sPort = sPort
        self.rAddress = rAddress
        self.rPort = rPort
        self.rStor = rStor
        self.sStor = sStor
        if sSock is None:
            self.sSock = socket.socket()
        else:
            self.sSock = sSock
        if rSock is None:
            self.rSock = socket.socket()
        else:
            self.rSock = rSock

    def run(self):
        print(self.receiveAscii())
        sleep(1)
        print(self.sendAscii(self.rStor))

    def sendAscii(self, msg):
        self.sSock.connect((self.sAddress, self.sPort))
        self.sSock.sendall(msg.encode("ascii"))
        sleep(1)
        self.sSock.close()
        return "sSock closed on client"

    def receiveAscii(self):
        self.rSock.bind((self.rAddress, self.rPort))
        self.rSock.listen(1)
        while True:
            connection, client_address = self.rSock.accept()
            final = b""
            try:
                while True:
                    partial = connection.recv(16)
                    if partial:
                        final += partial
                    else:
                        print(final.decode("ascii"))
                        break
            finally:
                connection.close()
                self.rStor = final.decode("ascii")
            break
        self.rSock.close()
        return "rSock closed on server"


srv = sysServer("localhost", 9998, "localhost", 9999)
cli = sysClient("hello!", "localhost", 9999, "localhost", 9998)
srv.start()
cli.start()
sleep(10)
del srv
del cli
