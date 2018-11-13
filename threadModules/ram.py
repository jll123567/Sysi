# random access memory
# module type: def
# [ w/e ,...]


# ram for threads
# storage([])
class ram:
    def __init__(self, storage=None):
        if storage is None:
            self.storage = []
        else:
            self.storage = storage

    # loads <dta> into ram
    # dta(any)*
    # none
    def load(self, dta):
        self.storage.append(dta)

    # reads <obj>'s ram
    # none
    # none
    def read(self):
        for i in self.storage:
            print(i)

    # searches ram for <query> using re.search
    # query(any)*
    # console output(str)/queryIndex(int)
    def search(self, query):
        matched = True
        for i in self.storage:
            if i == query:
                return self.storage.index(i)
        if not matched:
            print("no results. try obj.sysh.thread.ram.read()")

    # removes the <index>th iem from ram
    # Inputs
    #   index(int) is the int-th item in ram
    #   index(None) removes the last (or -1st) item in ram
    #   index([])=[] sets ram to []
    #   index(else) error message
    # Out
    #   console output(str), none
    def free(self, index):
        if index is None:
            self.storage.pop(-1)
        elif not index:
            self.storage = []
        elif isinstance(index, int):
            self.storage.pop(index)
        else:
            print("invalid request")


# Info at run
if __name__ == "__main__":
    print("# random access memory\nmodule type: def\n[ w/e ,...]")
