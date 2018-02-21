# import
import object


# setup
def logTagAdd(obj):
    obj.tag.update({"evLog": "logTagAdd"})
    return obj


def loggingTest(obj):
    obj.tag["evLog"].append("loggingTest")
    return obj


# runtime
if __name__ == "__main__":
    t = object.object(None, None, {"name": "test"})
    t = logTagAdd(t)
    t = loggingTest(t)
    print(t.tag)
