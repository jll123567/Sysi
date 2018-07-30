# setup
# queue
# format[task one,two,[sub one,sub two]]
# instruction="i/e : task"
# e is for exact code like tasks and i is for general strings


# noinspection PyDefaultArgument
class que:
    def __init__(self, tasks=[]):
        self.tasks = tasks

    def close(self):
        self.tasks = []

    def add(self, task):
        self.tasks.append(task)

    def interrupt(self, task, index):
        self.tasks.insert(index, task)

    def complete(self, i=None):
        if i is None:
            self.tasks.pop(0)
        else:
            self.tasks.pop(i)

    def showTask(self):
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

        for i in self.tasks:
            recurse(i, 0)


# noinspection SpellCheckingInspection
def makeValidTskProfile(queue):
    if isinstance(queue, que):
        tasks = queue.tasks
    else:
        tasks = queue
    # flatten function by rightfootin
    # snippet link: https://rightfootin.blogspot.com/2006/09/more-on-python-flatten.html
    #   modified to not include nested tuples as queues only support lists (or at least they're supposed to)
    mainTask = []
    for item in tasks:
        if isinstance(item, list):
            mainTask.extend(makeValidTskProfile(item))
        else:
            mainTask.append(item)
    return mainTask


# runtime
if __name__ == "__main__":
    print("queue v11.0")
