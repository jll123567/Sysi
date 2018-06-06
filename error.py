# import
import object


# setup
# err({"code":"type severeity:message", "resolutions":["opt0", ...], "selected": int})
# type : 0 resolved 1 warning 2 error immediate action required
# severeity: 0 resolved 1 low 2 med 3 high 4 critical 5 fatal
# message: string to describe the issue
# resolutions: what can be done to fix the issue
# selected: an integar that is the index of the resolution you want(None if no resolution selected) ex: want b [a,b,c,d] selected:1
class err(object.data):
    def __init__(self, errType, severity, message, resolutions, selected, tag):
        self.errDta = {"code": (str(errType) + str(severity) + ":" + message),
                       "resolutions": resolutions,
                       "selected": selected}
        self.tag = tag

    def setError(self, errType, severity, message, resolutions, selected):
        self.errDta["code"](str(errType) + str(severity) + ":" + message)
        self.errDta["resolutions"] = resolutions
        self.errDta["selected"] = selected

    def clearError(self):
        self.errDta = None

    def resolveError(self):
        resolveing = True
        print(self.errDta["code"])
        count = 0
        for i in self.errDta["resolutions"]:
            print(str(count) + ":" + i)
            count += 1
        while resolveing:
            try:
                selected = input("resolution?:")
                self.errDta["selected"] = int(selected)
            except ValueError:
                print("int only")
            else:
                resolveing = False
        print(self.errDta, self.tag)


# Runtime
if __name__ == "__main__":
    print("err v10.0")
