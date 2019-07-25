"""don't mind me, just being dumb"""
import pickle
import re


class c:
    def __init__(self, stor):
        self.stor = stor

    def read(self):
        return self.stor


a = c("yeet")
print(a)
b = pickle.dumps(a)
print(b)
d = "obj:"+b.hex()
print(d)
e = None
if re.match(r"obj:.*", d):
    e = pickle.loads(bytearray.fromhex(re.split(r":", d)[1]))
    print(e, e.read())
