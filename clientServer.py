import pickle
import re
import socket
import threading
import time


class sysSock(threading.Thread):
    """
    Handle data from individual sockets.
        All data should be either bytes or ascii strings.

    address is the hostname or ip address to connect/listen.
    port: the port to connect/listen.
    isSending: false for receiving and true for sending.
    data: when sending(self.isSending=True) this is the data sent.
        When receiving self.data should be what was received.
    dataType: a string to describe how to handle data.
    sock: the actual socket
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
        """Run the socket code."""
        while self.live:  # Let the thread die when specified.
            if self.isSending:  # See if the sock should send or receive data.
                self.sock = socket.socket()
                attemptConnect = True
                while attemptConnect:  # Try and connect and send data.
                    try:
                        self.sock.connect((self.address, self.port))
                        attemptConnect = False
                    except ConnectionRefusedError:
                        attemptConnect = True
                if self.dataType == "obj":  # Encode data.
                    pickledData = pickle.dumps(self.data)
                    toSend = "obj:{0}".format(pickledData.hex())
                elif self.dataType == "shift":
                    pickledData = pickle.dumps(self.data[0])
                    toSend = "shift:{0}:{1}".format(pickledData.hex(), self.data[1])
                elif self.dataType == "newConnection":
                    toSend = "newConnection:{0}:{1}:{2!s}".format(self.data[0], self.data[1], self.data[2])
                else:
                    break
                toSend = (toSend + ":end").encode("ascii")
                self.sock.sendall(toSend)  # YEET that data.
                self.sock.close()
                self.dataType = "finished"
                self.data = None
            else:
                self.sock = socket.socket()
                self.sock.bind((self.address, self.port))
                self.sock.listen(1)
                final = b""
                connection, clientAddress = self.sock.accept()  # Wait for a connection.
                try:
                    getting = True
                    while getting:
                        partial = connection.recv(16)
                        final += partial
                        if re.match(r".*:end", final.decode("ascii")) or not partial:  # Break on end of data or b''.
                            final = final[:-4]
                            getting = False
                finally:
                    connection.close()
                pair = re.split(r":", final.decode("ascii"))
                self.dataType = pair[0]
                pair.pop(0)
                self.data = pair
                if self.dataType == "obj":  # Decode data and store it.
                    self.data = pickle.loads(bytearray.fromhex(self.data[0]))
                elif self.dataType == "shift":
                    self.data[0] = pickle.loads(bytearray.fromhex(self.data[0]))
                elif self.dataType == "newConnection":
                    # noinspection PyTypeChecker
                    self.data[2] = int(self.data[2])
        self.sock.close()  # Kill the sock if the sysSock is to die.


class sysClient(threading.Thread):
    """
    Handles a client connection to a sysServer object. Each client corresponds to an object on the server.
    Thus the client's purpose is to control that object.

    Each client needs a unique Id.
    objId: the object to control.
    serverAddress and serverPort: holds the server ip address and port.
    selfAddress and selfPort: holds the current ip address and the port you would like to use.
    obj: a copy of the object from the server.
    nextShift: holds queued shifts to send to the server.
    """
    def __init__(self, clientId, objId, serverAddress, serverPort, selfAddress, selfPort, obj=None, nextShift=None):
        """
        :param clientId: str
        :param objId: str
        :param serverAddress: str
        :param serverPort: int
        :param selfAddress: str
        :param selfPort: int
        :param obj: sys_objects.sysObject
        :param nextShift: list
        """
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
        """To run on clientStart."""
        self.startConnection()  # Start the connection to the server.
        while self.live:  # Let me kill the client.
            if self.rSock.dataType == "obj":  # Look for a sysObject in the receiving sock.
                self.obj = self.rSock.data
                self.displayObj()  # Lets see that object.
            self.rSock.dataType = "finished"
            self.rSock.data = None
            if self.nextShift:  # If available, send the next shift to the networked object.
                self.sendShift(self.nextShift[0])
                self.nextShift.pop(0)
            for sInd in reversed(range(self.sSock.__len__())):  # Send stuff to send.
                if self.sSock[sInd].dataType == "finished":
                    self.sSock[sInd].live = False
                    self.sSock.pop(sInd)

    def startConnection(self):
        """Start a connection to the server."""
        # newConnection:<cliId>:<addr>:<port>:end
        sock = sysSock(self.selfAddress, self.selfPort)
        sock.start()
        self.rSock = sock
        sock = sysSock(self.serverAddress, self.serverPort, True, [self.clientId, self.selfAddress, self.selfPort],
                       "newConnection")
        sock.start()
        self.sSock.append(sock)

    def sendShift(self, shift):
        """
        Start up a sock use it to send <shift>.
        :param shift: list
        """
        # shift:<shift>:<objId>:end
        dt = [shift, self.objId]
        sock = sysSock(self.serverAddress, self.serverPort, True, dt, "shift")
        sock.start()
        self.sSock.append(sock)

    def addNextShift(self, sh):
        """
        Add <sh> to self.Shift .
        :param sh: list
        """
        self.nextShift.append(sh)

    def displayObj(self):
        """Print various pieces of self.obj ."""
        if self.obj is not None:
            print("tsk:{}\n{}\nram:{}\nid:{}\ncliId:{}".format(self.obj.trd.tsk.current, self.obj.trd.tsk.profile,
                                                               self.obj.trd.ram.storage, self.obj.tag["id"],
                                                               self.clientId))


class sysServer(threading.Thread):
    """
    Runs directories, manages client connections.
    selfAddress and selfPort: holds the current ip address and the port you would like to use.
    dirs: a list of all the directories to start.
    clientIdLookupTable: stores clientId's and their receiving sysSocket address/port.
    """

    def __init__(self, selfAddress, selfPort, dirs=None, clientIdLookupTable=None):
        """
        :param selfAddress: str
        :param selfPort: int
        :param dirs: list
        :param clientIdLookupTable: dict
        """
        super().__init__()
        self.selfAddress = selfAddress
        self.selfPort = selfPort
        self.rSock = None
        self.dirs = dirs
        if clientIdLookupTable is None:
            self.clientIdLookupTable = {}
        else:
            self.clientIdLookupTable = clientIdLookupTable
        self.live = True
        self.sSock = []

    def run(self):
        """Run this at server start."""
        for dirr in self.dirs:  # Start all the dirs(and subsequently their session).
            dirr.start()
        sock = sysSock(self.selfAddress, self.selfPort)
        sock.start()
        self.rSock = sock
        del sock
        while self.live:  # Let the server die if needed.
            if self.rSock.dataType == "shift":  # Deal with shifts.
                self.giveShift(self.rSock.data[0], self.rSock.data[1])
                self.rSock.data = None
                self.rSock.dataType = "finished"
            elif self.rSock.dataType == "newConnection":  # Deal with new connections.
                self.registerNewConnection()
                self.rSock.data = None
                self.rSock.dataType = "finished"
            else:
                pass
            for dirr in self.dirs:  # Handle server posts (networked objects)
                if dirr.serverPost:
                    for postInd in reversed(range(dirr.serverPost.__len__())):
                        alreadySending = False
                        for sock in self.sSock:
                            try:
                                if sock.data.tag["id"] == dirr.serverPost[postInd].tag["id"]:
                                    alreadySending = True
                            except AttributeError:
                                pass
                        if not alreadySending:
                            self.sendObj(dirr.serverPost[postInd])
                        dirr.serverPost.pop(postInd)
            for sInd in reversed(range(self.sSock.__len__())):  # Send all the things (that need to be send).
                if self.sSock[sInd].dataType == "finished":
                    self.sSock[sInd].live = False
                    self.sSock.pop(sInd)

    def giveShift(self, shift, objId):
        """
        Give <shift> to the object with <objId>.
        :param shift: list
        :param objId: str
        :return: None
        """
        for dirr in self.dirs:
            dirr.giveShift(shift, objId)

    def registerNewConnection(self):
        """
        Add an entry to self.clientIdLookupTable.
        :return: None
        """
        # noinspection PyShadowingNames
        cliId = self.rSock.data[0]
        addr = self.rSock.data[1]
        port = self.rSock.data[2]
        if isinstance(port, str):
            port = int(port)
        self.clientIdLookupTable.update({cliId: (addr, port)})

    def sendObj(self, obj):
        """
        Send a copy of <obj> to its corresponding client.
        :param obj: sys_objects.sysObject
        :return: None
        """
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
    # I'm just a test script. Ignore me.
    import sys_objects
    import CGE

    cli0Id = "cli/0"
    cli1Id = "cli/1"
    objA = sys_objects.sysObject()
    objA.tag.update({"id": "o/a", "permissions": {"sayHi": "allowed"}, "networkObject": cli0Id})
    objA.blankTask()
    objB = sys_objects.sysObject()
    objB.tag.update({"id": "o/b", "permissions": {"sayHi": "allowed"}, "networkObject": cli1Id})
    objB.blankTask()
    ses0 = CGE.CGESession("un/ses0", [objA, objB], ['c', False])
    dir0 = CGE.sessionDirectory("dr/dir0", [ses0])
    srv = sysServer("localhost", 9999, dirs=[dir0])
    srv.start()
    time.sleep(1)
    cli0 = sysClient(cli0Id, objA.tag["id"], "localhost", 9999, "localhost", 9998)
    cli0.start()
    time.sleep(.2)
    cli1 = sysClient(cli1Id, objB.tag["id"], "localhost", 9999, "localhost", 9997)
    cli1.start()
