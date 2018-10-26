# queuing for tasks in a general format
# module type: def
# format[task one,two,[sub one,sub two]]
# instruction="i/e : task"
# e is for exact code like tasks and i is for general strings


# thread module queue
# tasks([])
class que:
    def __init__(self, tasks=None):
        if tasks is None:
            self.tasks = []
        else:
            self.tasks = tasks

    # empty queue
    # none
    # none
    def close(self):
        self.tasks = []

    # insert a task at an index
    # task(task(str)*, index(int)
    # none
    def interrupt(self, task, index=0):
        self.tasks.insert(index, task)

    # complete a ask
    # index(int)
    # none
    def complete(self, index=None):
        if index is None:
            self.tasks.pop(0)
        else:
            self.tasks.pop(index)

    # show that tasks in the queue
    # none
    # console output(str)
    def showTask(self):
        # iterates through that thatThingThat'sAListOfThings and recursively adds indents
        # thatThingThat'sAListOfThings([])*, indent(int)*
        # console output(str)
        # noinspection SpellCheckingInspection
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


# make exact exact tasks into a valid tsk profile(broken at the moment) TODO fix make valid tsk profile
# queue(trd.queue)*
# tsk profile(trd.tsk)
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


# info at run
if __name__ == "__main__":
    print("queuing for tasks in a general format\nmodule type: def\nformat[task one,two,[sub one,"
          "sub two]]\ninstruction=\"i/e : task\"\ne is for exact code like tasks and i is for general strings")
