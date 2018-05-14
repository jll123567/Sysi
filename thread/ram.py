# import
import re


# setup
# random access memory
# [ w/e ,...]

class ram:
    def __init__(self, storage):
        self.storage = storage

    # loads <dta> into ram
    # use: <obj> = Sysh.thread.ram.laod(<obj>, <any>)
    # requires: obj
    def load(self, dta):
        self.storage.append(dta)

    # reads <obj>'s ram
    # use: Sysh.thread.ram.read(<obj>)
    # requires: obj
    def read(self):
        for i in self.storage:
            print(i)

    # searches ram for <query> using re.search
    # use: <obj> = Sysh.thread.ram.search(<obj>, <str or other re useable match>)
    # requires: obj
    def search(self, query):
        matched = True
        for i in self.storage:
            if re.search(query, i):
                print(i)
                print(self.storage.index(i))
                matched = True
        if not matched:
            print("no results. try obj.sysh.thred.ram.read()")

    # removes the <index>th iem from ram
    # use: <obj> = Sysh.thread.ram.free(<obj>, <int, None, or string "all">)
    # requires: obj
    # Inputs
    #   int is the int-th item in ram
    #   None removes the last (or -1st) item in ram
    #   "all" sets ram to []
    def free(self, index):
        if index is None:
            self.storage.pop(-1)
        elif index == "all":
            self.storage = []
        else:
            self.storage.pop(index)


# runtime
if __name__ == "__main__":
    print("random access memory manager v10.0")
