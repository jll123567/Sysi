import pickle
import re
import socket
import threading
from time import sleep


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
                atmptConnect = True
                while atmptConnect:
                    try:
                        self.sock.connect((self.address, self.port))
                        atmptConnect = False
                    except ConnectionRefusedError:
                        atmptConnect = True
                if self.dataType == "obj":
                    pickledData = pickle.dumps(self.data)
                    toSend = "obj:{0}".format(pickledData.hex())
                elif self.dataType == "shift":
                    pickledData = pickle.dumps(self.data[0])
                    toSend = "shift:{0}:{1}".format(pickledData.hex(), self.data[1])
                elif self.dataType == "newConnection":
                    toSend = "newConnection:{0}:{1}:{2!s}".format(self.data[0], self.data[1], self.data[2])
                else:
                    break
                # print(toSend)
                toSend = (toSend + ":end").encode("ascii")
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
                pair = re.split(r":", final.decode("ascii"))
                self.dataType = pair[0]
                pair.pop(0)
                self.data = pair
                if self.dataType == "obj":
                    self.data = pickle.loads(bytearray.fromhex(self.data[0]))
                elif self.dataType == "shift":
                    self.data[0] = pickle.loads(bytearray.fromhex(self.data[0]))
                elif self.dataType == "newConnection":
                    # noinspection PyTypeChecker
                    self.data[2] = int(self.data[2])
        self.sock.close()


class sysClient(threading.Thread):
    def __init__(self, clientId, objId, serverAddress, serverPort, selfAddress, selfPort, obj=None, nextShift=None):
        super().__init__()
        self.clientId = clientId
        self.objId = objId
        self.serverAddress = serverAddress
        self.serverPort = serverPort
        self.selfAddress = selfAddress
        self.selfPort = selfPort
        self.obj = obj
        if nextShift is None:
            self.nextShift = []
        else:
            self.nextShift = nextShift

        self.sSock = []
        self.rSock = None
        self.live = True

    def run(self):
        self.startConnection()
        while self.live:
            if self.rSock.dataType == "obj":
                self.obj = self.rSock.data
            self.rSock.dataType = "finished"
            self.rSock.data = None
            if self.nextShift:
                for shInd in range(0, self.nextShift.__len__() - 1):
                    self.sendShift(self.nextShift[shInd])
            for sInd in range(0, self.sSock.__len__() - 1):
                if self.sSock[sInd].dataType == "finished":
                    self.sSock[sInd].live = False
                    self.sSock.pop(sInd)

    def startConnection(self):

        # newConnection:<cliId>:<addr>:<port>:end
        sock = sysSock(self.selfAddress, self.selfPort)
        sock.start()
        self.rSock = sock
        print("trying to newConnect")
        sock = sysSock(self.serverAddress, self.serverPort, True, [self.clientId, self.selfAddress, self.selfPort],
                       "newConnection")
        sock.start()
        self.sSock.append(sock)

    def sendShift(self, shift):

        # shift:<shift>:<objId>:end
        dt = [shift, self.objId]
        sock = sysSock(self.serverAddress, self.serverPort, True, dt, "shift")
        sock.start()
        self.sSock.append(sock)

    def setNextShift(self, sh):
        self.nextShift = sh

    # sendShift(serverAddress, shift, objId)
    # dispObj(obj)
    # readReceive()


class sysServer(threading.Thread):
    """
    Runs directories, manages client connections.
    """

    def __init__(self, selfAddress, selfPort, rSock=None, dirs=None, clientIdLookupTable=None):
        super().__init__()
        self.selfAddress = selfAddress
        self.selfPort = selfPort
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
        self.sSock = []

    def run(self):
        for dirr in self.dirs:
            dirr.start()
        sock = sysSock(self.selfAddress, self.selfPort)
        sock.start()
        self.rSock = sock
        del sock
        while self.live:
            print("server:{}".format(self.sSock.__len__()))
            if self.rSock.dataType == "shift":
                self.giveShift(self.rSock.data[0], self.rSock.data[1])
            elif self.rSock.dataType == "newConnection":
                self.registerNewConnection()
            self.rSock.data = None
            self.rSock.dataType = "finished"
            for dirr in self.dirs:
                if dirr.serverPost:
                    if dirr.serverPost.__len__() < 10:
                        for _ in range(0, dirr.serverPost.__len__() - 1):
                            self.sendObj(dirr.serverPost[0])
                            dirr.serverPost.pop(0)
                    else:
                        for _ in range(0, 9):
                            self.sendObj(dirr.serverPost[0])
                            dirr.serverPost.pop(0)
            inds = []
            for sInd in range(0, self.sSock.__len__() - 1):
                if self.sSock[sInd].dataType == "finished":
                    inds.append(sInd)
                inds.sort(reverse=True)
                for i in inds:
                    self.sSock[i].live = False
                    self.sSock.pop(i)

    def giveShift(self, shift, objId):
        for dirr in self.dirs:
            dirr.giveShift(shift, objId)

    def registerNewConnection(self):
        # noinspection PyShadowingNames
        cliId = self.rSock.data[0]
        addr = self.rSock.data[1]
        port = self.rSock.data[2]
        if isinstance(port, str):
            port = int(port)
        self.clientIdLookupTable.update({cliId: (addr, port)})

    def sendObj(self, obj):

        # obj:<pickle dump as hex>:end
        # noinspection PyShadowingNames
        cliId = obj.tag["networkObject"]
        try:
            addr = self.clientIdLookupTable[cliId][0]
            port = self.clientIdLookupTable[cliId][1]
            sock = sysSock(addr, port, True, obj, "obj")
            sock.start()
            self.sSock.append(sock)
        except KeyError:
            pass


if __name__ == "__main__":
    import sys_objects
    import CGE

    cliId = "cli/0"
    a = sys_objects.sysObject()
    a.tag.update({"id": "o/a", "permissions": {"sayHi": "allowed"}, "networkObject": cliId})
    a.blankTask()
    b = CGE.CGESession("un/b", [a], ['c', False])
    c = CGE.sessionDirectory("dr/c", [b])
    srv = sysServer("localhost", 9999, dirs=[c])
    srv.start()
    sleep(1)
    cli = sysClient(cliId, a.tag["id"], "localhost", 9999, "localhost", 9998)
    cli.start()
