# import
import object


# setup
# err({"code":"type severeity:message", "resolutions":["opt0", ...], "selected": int})
# type : 0 resolved 1 warning 2 error immediate action required
# severeity: 0 resolved 1 low 2 med 3 high 4 critical 5 fatal
# message: string to describe the issue
# resolutions: what can be done to fix the issue
# selected: an integar that is the index of the resolution you want(None if no resolution selected) ex: want b [a,b,c,d] selected:1

def createError(errType, severity, message, resolutions, selected, name):
    e = object.storageata(
        {"code": (str(errType) + str(severity) + ":" + message), "resolutions": resolutions, "selected": selected},
        {"name": name, "relevancy": [0, 0, 0], "dataType": "err"})
    return e


def setError(err, errType, severity, message, resolutions, selected):
    err.storage["code"] = (str(errType) + str(severity) + ":" + message)
    err.storage["resolutions"] = resolutions
    err.storage["selected"] = selected
    return err


def clearError(err):
    err.storage = None
    err.tag["dataType"] = "none"


def resolveError(err):
    resolveing = True
    print(err.storage["code"])
    count = 0
    for i in err.storage["resolutions"]:
        print(str(count) + ":" + i)
        count += 1
    while resolveing:
        try:
            selected = input("resolution?:")
            err.storage["selected"] = int(selected)
        except ValueError:
            print("int only")
        else:
            resolveing = False
    print(err.storage, err.tag)
    return err


# Runtime
if __name__ == "__main__":
    print("err v10.0")
