"""random access memory"""
import prog.idGen


class ram:
    """holds random data the thread needs to store temporarily
    storage is a list that holds any"""
    def __init__(self, storage=None):
        """Initialize attributes
        Storage:[]"""
        if storage is None:
            self.storage = []
        else:
            self.storage = storage

    def load(self, dta):
        """put dta into self.storage"""
        self.storage.append(dta)

    def loadTrdDta(self, dta):
        """generate a generic id for dta and load() it"""
        dta.tag["id"] = prog.idGen.generateGenericId(self.storage, dta)
        self.load(dta)

    def read(self):
        """print the contents of self.storage to the console"""
        for i in self.storage:
            print(i)

    def search(self, query):
        """searched self.storage for query
        returns the index if the sysObject in storage and query are equal
        prints a message to the console if nothing was found"""
        matched = True
        idx = 0
        for i in self.storage:
            if i == query:
                return idx
            idx += 1
        if not matched:
            print("no results. try obj.trd.ram.read()")

    def free(self, index):
        """removes an sysObject from self.storage(with *style*)

        index(int) is the int-th item in self.storage
        index(None) removes the last (or -1st) item in ram
        index("all") sets ram to []
        index(else) print error to console"""
        if index is None:
            self.storage.pop(-1)
        elif index == "all":
            self.storage = []
        elif isinstance(index, int):
            self.storage.pop(index)
        else:
            print("invalid request")
