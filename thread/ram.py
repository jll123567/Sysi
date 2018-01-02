# import
import re
import object
import thread.memMgnt


# setup
# random access memory
# [ w/e ,...]

def load(obj, dta):
    obj.trd["ram"].append(dta)
    return obj


def read(obj):
    for i in obj.trd["ram"]:
        print(i)
    return obj


def search(obj, query):
    matched = True
    for i in obj.trd["ram"]:
        if re.search(query, i):
            print(i)
            print(obj.trd["ram"].index(i))
            matched = True
    if not matched:
        print("no results. try sysh.thred.ram.read(obj)")


def store(usr, storedRamName, storedRamImportance):
    dta = object.data([usr.trd["ram"]], {"name": storedRamName, "relevancy": [0, 0, storedRamImportance]})
    usr = thread.memMgnt.store(usr, 1, dta)
    return usr


def free(obj, index):
    if index is None:
        obj.trd["ram"].pop(-1)
    else:
        obj.trd["ram"].pop(index)
    return obj


# runtime
if __name__ == "__main__":
    print("random access memory manager v10.0")
