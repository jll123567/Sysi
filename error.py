# import
import object


# setup
# err({"code":"type severity:message", "resolutions":["opt0", ...], "selected": int})
# type : 0 resolved 1 warning 2 error immediate action required
# severity: 0 resolved 1 low 2 med 3 high 4 critical 5 fatal
# message: string to describe the issue
# resolutions: what can be done to fix the issue
# selected: an integer that is the index of the resolution you want(None if no resolution selected)
#
class err(object.data):
    def __init__(self, errType, severity, message, resolutions, selected, tag=None):
        if tag is None:
            tag = {"name": None}
        super().__init__(
            {"code": (str(errType) + str(severity) + ":" + message), "resolutions": resolutions, "selected": selected},
            tag)

    def setError(self, errType, severity, message, resolutions, selected):
        self.storage["code"](str(errType) + str(severity) + ":" + message)
        self.storage["resolutions"] = resolutions
        self.storage["selected"] = selected

    def clearError(self):
        self.storage = None

    def resolveError(self):
        resolving = True
        print(self.storage["code"])
        count = 0
        for i in self.storage["resolutions"]:
            print(str(count) + ":" + i)
            count += 1
        while resolving:
            try:
                selected = input("resolution?:")
                self.storage["selected"] = int(selected)
            except ValueError:
                print("int only")
            else:
                resolving = False
        print(self.storage, self.tag)


# Runtime
if __name__ == "__main__":
    print("err v11.0")
