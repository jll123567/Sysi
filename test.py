import threading
import time
import object
import threadModules.ram


class threadz(threading.Thread):
    def __init__(self, trdId, text, count):
        super().__init__()
        self.trdId = trdId
        self.text = text
        self.count = count

    def run(self):
        print("strating " + self.trdId)
        doIt(self)
        print("EOT @ " + self.trdId)


def doIt(thread):
    count = thread.count
    if count == 30:
        delay = 0.1
    else:
        delay = False
    while count > 0:
        if not delay:
            pass
        else:
            pass
            # time.sleep(delay)
        print(thread.text + ": x" + str(count))
        count -= 1
    print(thread.trdId + ": woot")


model0 = object.object()
model0.trd.ram = threadModules.ram.ram()
model0.trd.ram.storage.append("mama")
model1 = object.object()
model1.trd.ram = threadModules.ram.ram()
model1.trd.ram.storage.append("dada")
string = [threadz("trd0", "a", 20), threadz("trd1", "b", 30)]

string[0].start()
string[1].start()
print("EOF")
