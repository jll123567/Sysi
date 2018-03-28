# import
import re
import object
import thread.memMgnt


# setup
# random access memory
# [ w/e ,...]

# loads <dta> into ram
# use: <obj> = Sysh.thread.ram.laod(<obj>, <any>)
# requires: obj
def load(obj, dta):
    obj.trd["ram"].append(dta)
    return obj


# reads <obj>'s ram
# use: Sysh.thread.ram.read(<obj>)
# requires: obj
def read(obj):
    for i in obj.trd["ram"]:
        print(i)


# searches ram for <query> using re.search
# use: <obj> = Sysh.thread.ram.search(<obj>, <str or other re useable match>)
# requires: obj
def search(obj, query):
    matched = True
    for i in obj.trd["ram"]:
        if re.search(query, i):
            print(i)
            print(obj.trd["ram"].index(i))
            matched = True
    if not matched:
        print("no results. try sysh.thred.ram.read(obj)")


# saves a copy of ram ro memory
# use: <usr> = Sysh.thread.ram.store(<usr>, <string>, <int between 0 and 100>)
# requires: usr
def store(usr, storedRamName, storedRamImportance):
    dta = object.data([usr.trd["ram"]], {"name": storedRamName, "relevancy": [0, 0, storedRamImportance]})
    usr = thread.memMgnt.store(usr, 1, dta)
    return usr


# removes the <index>th iem from ram
# use: <obj> = Sysh.thread.ram.free(<obj>, <int, None, or string "all">)
# requires: obj
# Inputs
#   int is the int-th item in ram
#   None removes the last (or -1st) item in ram
#   "all" sets ram to []
def free(obj, index):
    if index is None:
        obj.trd["ram"].pop(-1)
    elif index == "all":
        obj.trd["ram"] = []
    else:
        obj.trd["ram"].pop(index)
    return obj


# runtime
if __name__ == "__main__":
    print("random access memory manager v10.0")
