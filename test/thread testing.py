# import
import thread.complex
import thread.damage
import object
import thread.language
import thread.memMgnt
import thread.move
import thread.ram
import thread.transfer

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
# test after you change things

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


def movTest(movObj):
    print(movObj.tag["previous location"])
    movObj = thread.move.move(movObj)
    print(movObj.trd["mov"])


# tread.move.moveto seems broken (in 3,4,5 out 3,3,3) fix it
# movTest(movObj)

# If you think im going to test my joke phys module you are WRONG


# ram testing
ramStore = object.object("irrelevant", {"ram": []}, {"name": "ramStore"})


def ramTest(ramStore):
    ramStore = thread.ram.load(ramStore, "hi")
    ramStore = thread.ram.load(ramStore, "hi1")
    thread.ram.read(ramStore)
    ramStore = thread.ram.free(ramStore, None)
    print(ramStore.trd["ram"])


# ramTest(ramStore)

# Tasker tested recently-ish just needs reformattiong

# transfer
iface0 = object.object("irrelevant", {"trnsf": None}, {"name": "iface0"})
iface1 = object.object("irrelevant", {"trnsf": object.data("hello", {"name": "dataToSend", "sender": None})},
                       {"name": "iface1"})


def sendTest(if0, if1):
    if0 = thread.transfer.send(if0, if1, if1.trd["trnsf"])
    print("\n", if0.trd["trnsf"].d)


# sendTest(iface0, iface1)


# Visual is sooooooooo broken so Ill just redo it at this point
# Its time woo
