# import
import thread.complex
import thread.damage
import object
import thread.language
import thread.memMgnt
import thread.move
import thread.ram
import thread.transfer
import thread.tasker

# TODO:
# ~~thread.complex.solve does not do anything, ill fix it later
# ~~standardize stat names with \standards_and_profiles\RPGStats.py
# ~~make stat dmg work, srsly
# ~~listen makes an ifinete loop, fix it
# ~~tread.move.moveto seems broken (in 3,4,5 out 3,3,3) fix it
# ~~add SO MANY COMMENTS, DOCUMENT
# ~~ram.free should be able to be fully cleared with "all"
# ~~ram.read shouldnt return anything
# ~~ram.free is freaking out about an empty list see if above is the issue
# ~~on tasker.await and tasker.react shoulndt use usr as an input and should use a profile.
# ~~transfer.send should dict.update rather than ["sender"] = <w/e>
# ~~transfer.receve should be removed
# ~~transfer should use transf not trnsf for its label
# ~~also obj.trd[<this thing>] is called a thread label
# ~~visual sucks, fix it PLEASE
# ~~test after you change things

# cpx test
cpxTest = object.object("mod not relevant", {"cpx": [[], []]}, {"name": "cpxTest"})


def cpxTst(probSolver):
    print("init val\n", probSolver.trd["cpx"])
    probSolver = thread.complex.newProblem(probSolver, "test Unsolved")
    probSolver = thread.complex.newProblem(probSolver, 0)
    probSolver = thread.complex.newProblem(probSolver, [0, 3])
    probSolver = thread.complex.newProblem(probSolver, True)
    print("add sol\n", probSolver.trd["cpx"])
    probSolver = thread.complex.postSolution(probSolver, "double check", 0)
    print("add sol\n", probSolver.trd["cpx"])


# cpxTst(cpxTest)


# dmg test
dmgTest = object.weapon("irrelevant", "", [[20, "atk"], [5, "def"]], {"name": "testWep"})
punchingBag = object.object("irrelevant", "irrelevant", {"name": "punching bag", "stat": {"def": 10}, "health": 100})


def dmgTst(wep, objToPunch):
    print("init\n", objToPunch.tag["health"], "\ndef: ", objToPunch.tag["stat"]["def"])
    objToPunch = thread.damage.stat(wep, objToPunch, 1)
    print("new def: ", objToPunch.tag["stat"]["def"])
    objToPunch = thread.damage.attack(wep, objToPunch)
    print("after hit(80)\n", objToPunch.tag["health"])


# dmgTst(dmgTest, punchingBag)


# langtest
listener = object.user("irrelevant", {"lang": [[[100, 100, 100], [100, 0, 0]], [0, 0, 0]], "ram": []},
                       "irrelevant", "irrelevant", {"name": "listener"})


# Ok ill figue out how to make listen work a SOME point but I dont want to rewright the entire thing so
# later
def langTest(listener):
    print(listener.trd["ram"])
    listener = thread.language.store(listener)
    print(listener.trd["ram"])


# langTest(listener)

# memMgnt
memBank = object.user("irreevant", {"ram": []}, "irrelevant", [0, ["start"], 2], {"name": "memBank",
                                                                                  "adminNote": "sorry"})


# testFunct
def memTest(usr):
    print(usr.trd, "\n  ", usr.mem)
    usr = thread.memMgnt.load(usr, 1, 0)
    print(usr.trd, "\n  ", usr.mem)
    usr = thread.memMgnt.forget(usr, 1, 0)
    print(usr.mem)
    usr = thread.memMgnt.store(usr, 1, "test0")
    print(usr.mem)
    usr = thread.memMgnt.modify(usr, 1, 0, "test1")
    print(usr.mem)


# memTest(memBank)

# move testing
movObj = object.object("irrelevant", {"mov": [0, 0, 0, 1, 1, 1]}, {"name": "movObj",
                                                                            "previous location": [0, 0, 0]})


def movTest(moveableObj):
    print(moveableObj.trd["mov"], "\n move +1,+1,+1")
    moveableObj = thread.move.move(moveableObj)
    print(moveableObj.trd["mov"], "\n warp to -10,0,0")
    moveableObj = thread.move.warp(moveableObj, -10, 0, 0)
    print(moveableObj.trd["mov"], "\n set acceleration 3,5,-20")
    moveableObj = thread.move.accelerate(moveableObj, 3, 5, -20)
    print(moveableObj.trd["mov"], "\n move +3,+5,-20")
    moveableObj = thread.move.move(moveableObj)
    print(moveableObj.trd["mov"])


# tread.move.moveto seems broken (in 3,4,5 out 3,3,3) fix it
# movTest(movObj)

# If you think im going to test my joke phys module you are WRONG


# ram testing
ramStore = object.object("irrelevant", {"ram": []}, {"name": "ramStore"})
usrStore = object.user("irrelevant", {"ram": None}, None, [[], [], []], {"name": "usrstore"})


def ramTest(ramObj, ramUsr):
    ramObj = thread.ram.load(ramObj, "hi")
    ramObj = thread.ram.load(ramObj, "hi1")
    thread.ram.read(ramObj)
    ramObj = thread.ram.free(ramObj, "all")
    ramObj = thread.ram.load(ramObj, "ma name jef")
    ramUsr.trd["ram"] = ramObj.trd["ram"]
    ramUsr = thread.ram.store(ramUsr, "jeff's name", 20)
    print(ramUsr.mem[1][0].d)
    print(ramObj.trd["ram"])


# ramTest(ramStore, usrStore)

# Tasker
taskObj = object.user("irrelevant",
                      {"tsk": [["test", "test1", "test2"], ["test", "test1", "test2"], ["I sould not be current"]],
                       "ram": []},
                      "irrelevant", [[], [], []], {"name": "taskObj"})


def tskTest(taskedObj):
    print(taskedObj.trd["tsk"])
    taskedObj = thread.tasker.step(taskedObj)
    taskedObj = thread.tasker.step(taskedObj)
    taskedObj = thread.tasker.step(taskedObj)
    print(taskedObj.trd["tsk"])
    taskedObj = thread.tasker.run(taskedObj)
    print(taskedObj.trd["tsk"])
    taskedObj = thread.tasker.addProfile(taskedObj, ["oh hi"])
    taskedObj = thread.tasker.setCurrentProfile(taskedObj, ["im here too"])
    taskedObj = thread.tasker.addProfile(taskedObj, ["oh hi"])
    print(taskedObj.trd["tsk"])
    taskedObj = thread.tasker.quitTask(taskedObj, -1)
    print(taskedObj.trd["tsk"])
    for i in range(0, 10):
        if i == 2:
            taskedObj = thread.tasker.wait(taskedObj, 5)
        else:
            print("b \n")
    print(taskedObj.trd["tsk"])


# tskTest(taskObj)


# transfer
iface0 = object.object("irrelevant", {"transf": None}, {"name": "iface0"})
iface1 = object.object("irrelevant", {"transf": object.data("hello", {"name": "dataToSend", "sender": None})},
                       {"name": "iface1"})


def sendTest(if0, if1):
    if0 = thread.transfer.send(if0, if1, if1.trd["transf"])
    print("\n", if0.trd["transf"].d)


# sendTest(iface0, iface1)


# Visual is sooooooooo broken so Ill just redo it at this point
# Its time woo
