# obj error and warn handling
# module type: def

import time


# err
# errType(int[0,2]), severity(int[0,5]), message(str), resolutions([str]), selected(None/int), tag(tag)
# type : 0 resolved 1 warning 2 error immediate action required
# severity: 0 resolved 1 low 2 med 3 high 4 critical 5 fatal
# message: string to describe the issue
# resolutions: what can be done to fix the issue
# selected: an integer that is the index of the resolution you want(None if no resolution selected)
class err:
    def __init__(self, errType=None, severity=None, message=None, resolutions=None, selected=None, obj=None, cont=None,
                 tag=None):
        if resolutions is None:
            self.resolutions = []
        else:
            self.resolutions = resolutions
        if selected is None:
            self.selected = []
        else:
            self.selected = selected
        if tag is None:
            self.tag = {"name": None, "id": None}
        else:
            self.tag = tag
        self.errType = errType
        self.severity = severity
        self.message = message
        self.obj = obj
        self.cont = cont
        self.timeRaised = time.clock()

    # set the error
    # errType(int[0,2])*, severity(int[0,5])*, message(str)*, resolutions([str])*, selected(None/int)*
    # none
    def setError(self, errType, severity, message, resolutions, selected, obj, cont):
        self.errType = errType
        self.severity = severity
        self.message = message
        self.obj = obj
        self.cont = cont
        self.resolutions = resolutions
        self.selected = selected

    # clear the error
    # none
    # none
    def clearError(self):
        self.resolutions = None
        self.selected = None
        self.errType = None
        self.severity = None
        self.message = None
        self.obj = None
        self.cont = None

    # attempt resolution
    # none
    # console output(str)
    def resolveError(self):
        resolving = True
        print(self.errType + ',' + self.severity + ':' + self.message)
        count = 0
        for resolution in self.resolutions:
            print(str(count) + ":" + resolution)
            count += 1
        while resolving:
            try:
                selected = input("resolution?:")
                self.selected = int(selected)
            except ValueError:
                print("int only")
            else:
                resolving = False


# info at run
if __name__ == "__main__":
    print("# obj error and warn handling\nmodule type: def")
