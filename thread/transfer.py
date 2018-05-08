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


# Baised off: https://docs.python.org/3/howto/sockets.html
def makeSocketInterface(interface)

def connect(interface, host, port):
        interface.connect((host, port))

def sendAscii(obj, msg):
        msg = msg.encode("ascii")
        totalsent = 0
        while totalsent < len(msg):
            sent = obj.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

def receive(obj):
        chunks = []
        bytes_recd = 0
        while bytes_recd < 254:
            chunk = obj.sock.recv(min(254 - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return b''.join(chunks)

def disconnect(self):
        self.sock.close()


# runtime
if __name__ == "__main__":
    print("basic transfer protocol v10.0")