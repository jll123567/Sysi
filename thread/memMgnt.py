# import
import re
import thread.ram


# setup
# mem[internal,real,storage]
# [obj,obj,...]stored in order of date added
def load(usr, block, index):
    if dir == 0:
        print("no internal access")
    else:
        usr = thread.ram.load(usr, usr.mem[block][index])
    return usr


def forget(usr, block, index):
    if block == 0:
        print("no internal access")
    else:
        usr.mem[block].pop(index)
    return usr


def store(usr, block, obj):
    if block == 0:
        print("no internal access")
    else:
        usr.mem[block].append(obj)
    return usr


def find(usr, query):
    if query is None:
        query = input()
    for d in range(1, 2):
        for i in usr.mem[d]:
            for t in i.tag:
                if re.match(str(t), r"*(.)" + query + r"*(.)"):
                    print(t)
                else:
                    print(None)


def modify(usr, block, index, value):
    if block == 0:
        print("no internal access")
    else:
        usr.mem[block][index] = value
    return usr


# runtime
if __name__ == "__main__":
    print("user memory v10.0")