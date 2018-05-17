# import
import socket


# setup
# transf
# interface = container for received data

class transf:
    def __init__(self, interface=None):
        self.interface = interface

    # sends <data> form an object to another
    # use <obj> = Sysh.thread.transfer.send(<obj>, <sender>, <dta>
    # requires: 2 obj (sender and obj) and dta
    def send(self, sender, dta):
        pkg = dta
        pkg.tag.update({"sender": sender.tag["name"]})
        self.interface = pkg

    # clears the interface
    # use obj = clearInterface(<obj>)
    # requires obj with transf interface
    def clearInterface(self):
        self.interface = None

    # socket code based off: https://docs.python.org/3/howto/sockets.html

    # sets <obj>'s transfer interface to a socket
    # use <obj> = Sysh.thread.transfer.makeSocketInterface(<obj>)
    # requires obj with a transfer interface (<obj>.trd["transf"])
    def makeSocketInterface(self):
        self.interface = socket.socket()

    # connects the socket to <host> at <port>
    # use connectSocket(<interface>, <host>, <port>)
    # requires socket at <interface>
    def connectSocket(self, host, port):
        self.interface.connect((host, port))

    # sends an ascii encoded message though the socket
    # use sendSocket(<interface>, <message>)
    # requires socket at <interface>
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
    print("basic transfer protocol v10.0")
