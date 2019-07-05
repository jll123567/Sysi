"""don't mind me, just being dumb"""
import sys_objects
import CGE
import thread_modules


class sendableObj(sys_objects.sysObject):
    def __init__(self, m=None, tr=None, tg=None):
        super().__init__(m, tr, tg)
        self.trd.transf = thread_modules.Transfer()

    def generateSendRequest(self, dta, targetId):
        self.trd.transf.send(self.tag["id"], dta)
        request = [targetId, "acceptSendRequest", [self.trd.transf.interface], self.tag["id"]]
        self.trd.tsk.current.append(request)

    def acceptSendRequest(self, dta):
        print("aSR started")
        willReceve = False
        if dta.tag["sender"] is not None:
            willReceve = True
        if willReceve:
            acceptOp = [self.tag["id"], "receiveSendData", [dta], self.tag["id"]]
            self.trd.tsk.addOperation(acceptOp)
        print("aSR Finished")

    def receiveSendData(self, dta):
        self.trd.transf.receive(dta)

    def debugInterface(self):
        print(self.trd.transf.interface.storage)


b = sendableObj()
d = sendableObj()
dtaA = sys_objects.data("Hi")
dtaB = sys_objects.data("OverwriteMe")
b.tag["id"] = "o/b"
d.tag["id"] = "o/d"
d.trd.transf.interface = dtaB
b.generateSendRequest(dtaA, "o/d")
d.trd.tsk.current.append(["o/d.trd.tsk", "loopInf", [["o/d", "debugInterface", [], "o/d"]], "o/d"])
# d.trd.tsk.profile = [[]]
session = CGE.CGESession("f", [b, d], ["c", False])
session.start()
