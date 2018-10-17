# object data transfer
# module type: def
import socket


# transf
# interface(dta/socket)
class transf:
    def __init__(self, interface=None):
        self.interface = interface

    # package dta for sending
    # sender(objId)*, dta(dta)*
    # none
    def send(self, sender, dta):
        pkg = dta
        pkg.tag.update({"sender": sender})
        self.interface = pkg

    # receive data from an obj
    # sender(obj)*
    # none/console output(str)
    def receive(self, sender):
        try:
            self.interface = sender.trd.transf.interface
        except AttributeError:
            print("listed sender:" + str(sender.tag["name"]) + "'s transf interface was not found\ndoes it have a "
                                                               "trd.transf")

    # clears the interface
    # none
    # none
    def clearInterface(self):
        self.interface = None

    # socket code based off: https://docs.python.org/3/howto/sockets.html

    # sets <obj>'s transfer interface to a socket
    # none
    # none
    def makeSocketInterface(self):
        self.interface = socket.socket()

    # connects the socket to <host> at <port>
    # host(ip/hostname(str))*, port(int)*
    #
    def connectSocket(self, host, port):
        self.interface.connect((host, port))

    # sends an ascii encoded message though the socket
    #
    # todo continue
    def sendSocket(self, msg):
        msg = msg.encode("ascii")
        totalSent = 0
        while totalSent < len(msg):
            sent = self.interface.send(msg[totalSent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalSent = totalSent + sent

    # receives 254 bytes from the socket
    # use connectSocket(<interface>)
    # requires socket at <interface>
    def receiveSocket(self):
        chunks = []
        bytes_recd = 0
        while bytes_recd < 254:
            chunk = self.interface.recv(min(254 - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return b''.join(chunks)

    # closes the socket
    # use disconnectSocket(<interface>)
    # requires socket at <interface>
    def disconnectSocket(self):
        self.interface.close()


# runtime
if __name__ == "__main__":
    print("basic transfer protocol v11.0")
