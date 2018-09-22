# setup
# err({"code":"type severity:message", "resolutions":["opt0", ...], "selected": int})
# type : 0 resolved 1 warning 2 error immediate action required
# severity: 0 resolved 1 low 2 med 3 high 4 critical 5 fatal
# message: string to describe the issue
# resolutions: what can be done to fix the issue
# selected: an integer that is the index of the resolution you want(None if no resolution selected)


class err:
    def __init__(self, errType=None, severity=None, message=None, resolutions=None, selected=None, tag=None):
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
        self.errCode = [errType, severity, message]

    def setError(self, errType, severity, message, resolutions, selected):
        self.errCode = [errType, severity, message]
        self.resolutions = resolutions
        self.selected = selected

    def clearError(self):
        self.resolutions = None
        self.selected = None
        self.errCode = [None, None, None]

    def resolveError(self):
        resolving = True
        print(self.errCode[0] + ',' + self.errCode[1] + ':' + self.errCode[2])
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


# Runtime
if __name__ == "__main__":
    print("err v11.0")
