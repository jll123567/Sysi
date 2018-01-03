# import
import object
import thread.memMgnt


# setup
# queue
# format[task one,two,[sub one,sub two]]
# instruction="i/e : task"
# e is for exact code like tasks and i is for inexact string or english like tasks
def load(obj, memory):
    obj.trd["que"] = obj.mem[0][memory].d
    return obj


def close(obj):
    obj.trd["que"] = []
    return obj


def save(obj, tags):
    lastQueue = object.data(obj.trd["que"], tags)
    obj = thread.memMgnt.store(obj, 1, lastQueue)
    print("queue saved to: ", lastQueue, "@", obj.tag["name"], ".mem")
    return obj


def add(obj, task):
    obj.trd["que"].append(task)
    return obj


def interrupt(obj, task, index):
    obj.trd["que"].insert(index, task)
    return obj


def complete(obj, i):
    if i is None:
        obj.trd["que"].pop(0)
    else:
        obj.trd["que"].pop(i)
    return obj


def showTask(obj):
    def recurse(thatThingThatsAListOfThings, indent):
        if isinstance(thatThingThatsAListOfThings, list):
            recurse(thatThingThatsAListOfThings, indent + 1)
        else:
            if i[0] == "e":
                print("  " * indent, "exact:", thatThingThatsAListOfThings)
            elif i[0] == "i":
                print("  " * indent, "inexact:", thatThingThatsAListOfThings)
            else:
                print("Not a valid task type")
    for i in obj.trd["que"]:
        recurse(i, 0)


def makeValidTskProfile(Que):
    # flatten function by rightfootin
    # snippet link: https://rightfootin.blogspot.com/2006/09/more-on-python-flatten.html
    #   modified to not include nested tuples as queues only support lists (or at least they're supposed to)
    mainTask = []
    for item in Que:
        if isinstance(item, list):
            mainTask.extend(makeValidTskProfile(item))
        else:
            mainTask.append(item)
    return mainTask


# runtime
if __name__ == "__main__":
    print("queue v10.0")
