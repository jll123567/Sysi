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
        self.live = True

    def run(self):
        while self.live:
            if self.isSending:
                self.sock = socket.socket()
                self.sock.connect((self.address, self.port))
                if self.dataType == "obj":
                    pickledData = pickle.dumps(self.data)
                    toSend = "obj" + ':' + pickledData.hex()
                elif self.dataType == "shift":
                    pickledData = pickle.dumps(self.data[0])
                    toSend = "shift" + ':' + pickledData.hex() + ':' + self.data[1]
                else:
                    break
                toSend = (toSend+":end").encode("ascii")
                self.sock.sendall(toSend)
                self.sock.close()
                self.dataType = "unspecified"
                self.data = None
            else:
                self.sock = socket.socket()
                self.sock.bind((self.address, self.port))
                self.sock.listen(1)
                final = b""
                connection, clientAddress = self.sock.accept()
                try:
                    while True:
                        partial = connection.recv(16)
                        final += partial
                        if re.match(r".*:end", final.decode("ascii")):
                            final = final[:-4]
                            break

                finally:
                    connection.close()
                    self.sock.close()
                pair = re.split(r":", final.decode("ascii"))
                self.dataType = pair[0]
                pair.pop(0)
                self.data = pair
                if self.dataType == "obj":
                    self.data = pickle.loads(bytearray.fromhex(self.data[0]))
                elif self.dataType == "shift":
                    self.data[0] = pickle.loads(bytearray.fromhex(self.data[0]))


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
        self.live = True

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
        self.live = True

    def run(self):
        for dirr in self.dirs:
            dirr.start()
        while self.live:
            if self.rSock.dataType == "shift":
                self.giveShift(self.rSock.data[0], self.rSock.data[1])
                self.rSock.data = None
                self.rSock.dataType = "unspecified"

    def giveShift(self, shift, objId):
        for dirr in self.dirs:
            dirr.giveShift(shift, objId)
    # sendObj(obj,clientId)
    # readReceive()


if __name__ == "__main__":
    import sys_objects
    import CGE

    a = sys_objects.sysObject()
    a.tag["id"] = "o/a"
    a.tag["permissions"] = {"sayHi": "allowed"}
    a.blankTask()
    b = CGE.CGESession("un/b", [a], ['c', False])
    c = CGE.sessionDirectory("dr/c", [b])
    srv = sysServer(dirs=[c])
    srv.rSock = sysSock("localhost", 9999, False)
    srv.rSock.start()
    srv.start()
    cli = sysSock("localhost", 9999, True, [[["o/a", "sayHi", [], "o/a"]], "o/a"], "shift")
    cli.start()
