# import
import re
import hashlib
import object


# setup
# mem[internal,real,storage]
# [obj,obj,...]stored in order of date added

class mem:
    # noinspection PyDefaultArgument
    def __init__(self, internal=[], real=[], external=[]):
        self.internal = internal
        self.real = real
        self.external = external

    def forget(self, block, index):
        if block == 0:
            print("no internal access")
        elif block == 1:
            self.real.pop(index)
        else:
            self.external.pop(index)

    def store(self, block, obj):
        if block == 0:
            print("no internal access")
        elif block == 1:
            self.real.append(obj)
        else:
            self.external.append(obj)

    def find(self, query):
        if query is None:
            query = input()
        for d in self.__dict__:
            for i in d:
                if re.match(str(i), r"*(.)" + query + r"*(.)"):
                    print(i)
                else:
                    print(None)

    def modify(self, block, index, value):
        if block == 0:
            print("no internal access")
        elif block == 1:
            self.external[index] = value
        else:
            self.external[index] = value
    
    
# converts an object to a "hashed" (shortened data preserving tags)
def saveAsHash(obj):
    info = obj
    dta = object.data((hashlib.md5(info.encode('utf-8')).hexdigest()), obj.tag)
    return dta


# runtime
if __name__ == "__main__":
    print("atribs memory v11.0")
