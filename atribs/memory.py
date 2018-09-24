# Definition for user memory
# mod type: def
import re
import hashlib
import object


# User memory
# internal - for user created content
# real - for recorded events
# external - admin data pushing store
class mem:
    #
    def __init__(self, internal=None, real=None, external=None):
        if internal is None:
            self.internal = []
        else:
            self.internal = internal
        if real is None:
            self.real = []
        else:
            self.real = real
        if external is None:
            self.external = []
        else:
            self.external = external

    # Removes memories
    # block(int[0-2])*, index(int)*
    # No output
    def forget(self, block, index):
        if block == 0:
            print("no internal forgetting")
        elif block == 1:
            self.real.pop(index)
        else:
            print("requires direct mod")

    # adds a memory(obj)
    # block(in[0-2])*, obj(any)*
    # No output
    def store(self, block, obj):
        if block == 0:
            self.internal.append(obj)
        elif block == 1:
            self.real.append(obj)
        else:
            print("requires direct mod")

    # finds something that matched the query and prints it, if nothing is found, None is printed
    # query(str)
    # console output(str)
    def find(self, query=None):
        if query is None:
            query = input()
        for d in self.__dict__:
            for i in d:
                if re.match(str(i), r"*(.)" + query + r"*(.)"):
                    print(i)
                else:
                    print(None)

    # modified a memory
    # block(int[0-2])*, index(int)*, value(any)*
    def modify(self, block, index, value):
        if block == 0:
            print("no internal modify")
        elif block == 1:
            self.internal[index] = value
        else:
            print("requires direct mod")


# gives an md5 hash of obj
# obj(any)*
# dta(str[md5 Hash of obj])
def saveObjHash(obj):
    info = obj
    dta = object.data((hashlib.md5(info.encode('utf-8')).hexdigest()), obj.tag)
    return dta


# TODO: add checksum bc its more accurate


# info at run
if __name__ == "__main__":
    print("Definition for user memory\nmod type: def")
