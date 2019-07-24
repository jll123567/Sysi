# import sys_objects
# import CGE
import socket

# [send,recv]

# line 5, in <module>
#     client = {"send":socket.socket().connect(("localhost", 1566)),"recv":socket.socket().connect(("localhost", 1567))}
# ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it
client = {"send": socket.socket().connect(("localhost", 1566)), "recv": socket.socket().connect(("localhost", 1567))}
server = {"send": socket.socket().connect(("localhost", 1567)), "recv": socket.socket().connect(("localhost", 1566))}


def sendSocket(sock, msg):
    """
    Send ascii text.
    Raise a RuntimeError if the connection breaks.
    """
    msg = msg.encode("ascii")
    totalSent = 0
    while totalSent < len(msg):
        sent = sock.send(msg[totalSent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalSent = totalSent + sent


def receiveSocket(sock):
    """
    Grab 254 bytes from the socket.
    Raise a RuntimeError if the connection breaks.
    """
    chunks = []
    bytes_recd = 0
    while bytes_recd < 254:
        chunk = sock.recv(min(254 - bytes_recd, 2048))
        if chunk == b'':
            raise RuntimeError("socket connection broken")
        chunks.append(chunk)
        bytes_recd = bytes_recd + len(chunk)
    return b''.join(chunks)


serverMessage = "This is a test of of some sockets(ascii only)"
print("server: ", serverMessage)
print("sending")
# noinspection PyTypeChecker
sendSocket(server["send"], serverMessage)
print("sent?")
# noinspection PyTypeChecker
print("client: ", receiveSocket(client["recv"]))
print("this DIDN'T explode..!")
