# import
import socket
# setup
# transf
# interface = container for receved data


# sends <data> form an object to another
# use <obj> = Sysh.thread.transfer.send(<obj>, <sender>, <dta>
# requres: 2 obj (sender and obj) and dta
def send(obj, sender, dta):
    pkg = dta
    pkg.tag.update({"sender": sender.tag["name"]})
    obj.trd["transf"] = pkg
    return obj


# socket code based off: https://docs.python.org/3/howto/sockets.html

# sets <obj>'s transfer interface to a socket
# use <obj> = Sysh.thread.transfer.makeSocketInterface(<obj>)
# requires obj with a transfer interface (<obj>.trd["transf"])
def makeSocketInterface(obj):
    obj.trd["transf"] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return obj


# connects the socket to <host> at <port>
# use connectSocket(<interface>, <host>, <port>)
# requires socket at <interface>
def connectSocket(interface, host, port):
        interface.connect((host, port))


# sends an ascii encoded message though the socket
# use sendSocket(<interface>, <message>)
# requires socket at <interface>
def sendSocket(interface, msg):
        msg = msg.encode("ascii")
        totalsent = 0
        while totalsent < len(msg):
            sent = interface.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent


# receves 254 bytes from the socket
# use connectSocket(<interface>)
# requires socket at <interface>
def receiveSocket(interface):
        chunks = []
        bytes_recd = 0
        while bytes_recd < 254:
            chunk = interface.recv(min(254 - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return b''.join(chunks)


# closes the socket
# use disconnectSocket(<interface>)
# requires socket at <interface>
def disconnectSocket(interface):
        interface.close()


# clears the interface
# use obj = clearInterface(<obj>)
# requires obj with transf interface
def clearInterface(obj):
    obj.trd["transf"] = None
    return obj


# runtime
if __name__ == "__main__":
    print("basic transfer protocol v10.0")