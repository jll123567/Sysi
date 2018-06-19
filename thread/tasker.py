# import
import time


# setup
# tasker
# tsk=[profile,profile,profile,...]
# profile=[f0,f1,f2,...]
# first profile is current profile

# steps through each command in current profile
# use <obj> = Sysh.thread.tasker.step(<obj>)
# requires: obj
def step(obj):
    print(obj.trd["tsk"][0][0])
    obj.trd["tsk"][0].pop(0)
    if obj.trd["tsk"][0] == []:
        obj.trd["tsk"].pop(0)
    return obj


# runs entire profile
# use <obj> = Sysh.thread.tasker.run(<obj>)
# requires: obj
def run(obj):
    for i in obj.trd["tsk"][0]:
        print(i)
    obj.trd["tsk"].pop(0)
    return obj


# sets the current profile to <profile>
# use <obj> = Sysh.thread.tasker.setCurrentProfile(<obj>, <task profile>)
# requires: obj
def setCurrentProfile(obj, profile):
    obj.trd["tsk"].insert(0, profile)
    return obj


# adds a new profile to the end of the tasking queue
# use <obj> = Sysh.thread.tasker.addProflie(<obj>, <task profile>)
# requires: obj
def addProfile(obj, profile):
    obj.trd["tsk"].append(profile)
    return obj


# ends a task
# use <obj> = Sysh.thread.tasker.quitTask(<obj>, <index>)
# requires: obj
def quitTask(obj, index):
    obj.trd["tsk"].pop(index)
    return obj


# waits <t> seconds before running <obj>
# use <obj> = Sysh.thread.tasker.wait(<obj>, <int/float>)
# requires: obj
def wait(obj, t):
    time.sleep(t)
    obj = run(obj)
    return obj


# runtime
if __name__ == "__main__":
    print("tasker v11.0")
