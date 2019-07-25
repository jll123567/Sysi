import pickle
import re
import socket
import threading


# from time import sleep

# cli sShift rObj
# serv sObj rShift
#     runs dirs
#     keep track of clients
#

class sysSock(threading.Thread):
    """
    Handle data from individual sockets.
        All data should be either bytes or ascii strings.

    address is the hostname or ip address to connect/listen.
    port is the port to connect/listen.
    isSending is false for receiving and true for sending.
    data: when sending(self.isSending=True) this is the data sent.
        When receiving self.data should be what was received.
    dataType is a string to describe how to handle data.
    sock is the actual socket
    """

    def __init__(self, address, port, isSending=False, data=None, dataType=None, sock=None):
        """
        :param address: str
        :param port: int
        :param isSending: bool
        :param data: any
        :param dataType: string
        :param sock: socket.socket
        """
        super().__init__()
        self.sock = sock
        self.address = address
        self.port = port
        self.isSending = isSending
        if not self.isSending:
            self.data = None
        else:
            self.data = data
        if dataType is None:
            self.dataType = "unspecified"
        else:
            self.dataType = dataType

    def run(self):
        if self.isSending:
            self.sock = socket.socket()
            self.sock.connect((self.address, self.port))
            toSend = None
            if self.dataType == "obj":
                pickledData = self.data
                pickledData = pickle.dumps(pickledData)
                toSend = "obj" + ':' + pickledData.hex()
                toSend = toSend.encode("ascii")
            self.sock.sendall(toSend)
            self.sock.close()
        else:
            self.sock = socket.socket()
            self.sock.bind((self.address, self.port))
            self.sock.listen(1)
            final = b""
            while True:
                connection, clientAddress = self.sock.accept()
                try:
                    while True:
                        partial = connection.recv(128)
                        if partial:
                            final += partial
                        else:
                            break
                finally:
                    connection.close()
                    self.sock.close()
                    break
            pair = re.split(r":", final.decode("ascii"))
            self.dataType = pair[0]
            self.data = pair[1]
            if self.dataType == "obj":
                self.data = pickle.loads(bytearray.fromhex(self.data))


class sysClient(threading.Thread):
    def __init__(self, clientId, obj=None, nextShift=None):
        super().__init__()
        self.clientId = clientId
        self.obj = obj
        if nextShift is None:
            self.nextShift = []
        else:
            self.nextShift = nextShift
        self.sSock = None
        self.rSock = None

    def run(self):
        pass

    # sendShift(serverAddress, shift, objId)
    # dispObj(obj)
    # readReceive()


class sysServer(threading.Thread):
    """
    Runs directories, manages client connections.
    """

    def __init__(self, sSock=None, rSock=None, dirs=None, clientIdLookupTable=None):
        super().__init__()

        if sSock is None:
            self.sSock = socket.socket()
        else:
            self.sSock = sSock
        if rSock is None:
            self.rSock = socket.socket()
        else:
            self.rSock = rSock
        self.dirs = dirs
        if clientIdLookupTable is None:
            self.clientIdLookupTable = {}
        else:
            self.clientIdLookupTable = clientIdLookupTable

    def run(self):
        pass
    # giveShift(objId,shift)
    # sendObj(obj,clientId)
    # readReceive()


if __name__ == "__main__":
    class c:
        def __init__(self, stor):
            self.stor = stor

        def read(self):
            return self.stor

    cli = sysSock("localhost", 9999, True, c("yeet"), "obj")
    srv = sysSock("localhost", 9999)
    srv.start()
    cli.start()
