# tasker
# module type: def
import time
import object


# profile=[shift,shift,shift,...]
# shift=[op0,op1,op2,...]
# operation=[target(str), function(str), [parameters]]


# tasking
# current(tskShift), profiles(tskProfile)
class tsk:
    def __init__(self, current=None, profile=None):
        if current is None:
            self.current = []
        else:
            self.current = current
        if profile is None:
            self.profile = []
        else:
            self.profile = profile

    # moves next shift to current
    # none
    # none
    def nextCurrent(self):
        if self.profile:
            if isinstance(self.profile[0], list):
                self.current = self.profile[0]
            else:
                self.current = [self.profile[0]]
            self.profile.pop(0)
        else:
            self.current = []

    # prints the first operation in current
    # none
    # console output(str)
    # WARN:DTA LEAK
    def debugCurrentOp(self):
        print(self.current[0])

    # prints all current operations
    # none
    # console output(str)
    # WARN:DTA LEAK
    def debugCurrent(self):
        for operation in self.current:
            print(operation)
        self.nextCurrent()

    # sets the current shift
    # shift(tskShift)*
    # none
    def setCurrent(self, shift):
        self.current = shift

    # append an operation to the current shift
    # operation(tskOperation)*
    # none
    def appendCurrent(self, operation):
        self.current.append(operation)

    # adds a new shift to the end of the tasking queue
    # shift(tskShift)*
    # none
    def addProfile(self, shift):
        self.profile.append(shift)

    # removes a shift from the profile
    # index(int)*
    # none
    def removeShift(self, index):
        self.profile.pop(index)

    # waits <t> seconds before continuing
    # time(float)*
    # none
    @staticmethod
    def wait(t):
        time.sleep(t)

    # set the following shift to loop infinitely
    # shift(tskShift)
    # requires self
    def loopInf(self, shift):
        objId = ""
        for char in shift[0]:
            if char == '.':
                break
            else:
                objId += char
        objId += ".trd.tsk"
        self.addProfile([shift, [objId, "loopInf", [shift]]])

    # determine the next shift based on the state of object0 and object1(they don't need to be sysh.object.object s)
    # comparator("==","!=",">","<","<=",">=")*, object0(any)*, object1(any)*, then(tskShift)*, els(tskShift)
    # none/console output(str)
    def ifStatement(self, comparator, object0, object1, then, els=None):
        if not isinstance(then[0], list):
            then = [then]
        if comparator == '==':
            if object0 == object1:
                self.profile.insert(0, then)
            else:
                if els is not None:
                    self.profile.insert(0, els)
        elif comparator == '!=':
            if object0 != object1:
                self.profile.insert(0, then)
            else:
                if els is not None:
                    self.profile.insert(0, els)
        elif comparator == '>':
            if object0 > object1:
                self.profile.insert(0, then)
            else:
                if els is not None:
                    self.profile.insert(0, els)
        elif comparator == '<':
            if object0 < object1:
                self.profile.insert(0, then)
            else:
                if els is not None:
                    self.profile.insert(0, els)
        elif comparator == '>=':
            if object0 >= object1:
                self.profile.insert(0, then)
            else:
                if els is not None:
                    self.profile.insert(0, els)
        elif comparator == '<=':
            if object0 <= object1:
                self.profile.insert(0, then)
            else:
                if els is not None:
                    self.profile.insert(0, els)
        else:
            print("the comparator inputted is not valid")

    # print msg
    # msg(str)*
    # console output(str)
    @staticmethod
    def debugPrint(msg):
        print(msg)

    # pack data for ram
    # none
    # dta(tsk attribs, tags)
    def package(self):
        return object.data([self.current, self.profile], {"name": "tread.tsk.package", "id": None,
                                                          "dataType": "thread.tsk.package"})


# info at run
if __name__ == "__main__":
    print("tasker\nmodule type: def")
