# import
import thread.complex
import thread.damage
import object
import thread.language
import thread.memMgnt
import thread.move
import thread.ram

# TODO:
# thread.complex.solve does not do anything, ill fix it later
# standardize stat names with \standards_and_profiles\RPGStats.py
# make stat dmg work, srsly
# listen makes an ifinete loop, fix it
# tread.move.moveto seems broken (in 3,4,5 out 3,3,3) fix it
# add SO MANY COMMENTS, DOCUMENT DAMNIT
# ram.free should be able to be fully cleared with "all"
# ram.read shouldnt return anything
# ram.free is freaking out about an empty list see if above is the issue

# cpx test
cpxTest = object.object("mod not relevant", {"cpx": [[], None]}, {"name": "cpxTest"})


def cpxTst(cpxTest):
    print("init val\n", cpxTest.trd["cpx"])
    cpxTest = thread.complex.newProblem(cpxTest, "test Unsolved")
    cpxTest = thread.complex.newProblem(cpxTest, 0)
    cpxTest = thread.complex.newProblem(cpxTest, [0, 3])
    cpxTest = thread.complex.newProblem(cpxTest, True)
    print("add problem\n", cpxTest.trd["cpx"])
    cpxTest = thread.complex.post(cpxTest, "success")
    print("add sol\n", cpxTest.trd["cpx"])
    cpxTest = thread.complex.post(cpxTest, "double check")
    print("add sol\n", cpxTest.trd["cpx"])
    # thread.complex.solve does not do anything, ill fix it later


cpxTst(cpxTest)

# dmg test
# soon
dmgTest = object.weapon("irrelevant", "", [20, "health"], {"name": "testWep"})
# standardize stat names with \standards_and_profiles\RPGStats.py
punchingBag = object.object("irrelevant", "irrelevant", {"name": "punching bag", "stat": {"defence": 2, "health": 100}})


def dmgTst(dmgTest, punchingBag):
    print("init\n", punchingBag.tag["health"])
    punchingBag = thread.damage.stat(dmgTest, punchingBag)
    print("after hit(rough 82)\n", punchingBag.tag["health"])


# wow I cant even type
# dmgTst(dmgTest, punchingBag)


# langtest
listener = object.user("irrelevant", {"lang": [[[100, 100, 100], [100, 0, 0]], [0, 0, 0]], "ram": []},
                       "irrelevant", "irrelevant", {"name": "listener"})


# just store bc listen makes an ifinete loop
def langTest(listener):
    print(listener.trd["ram"])
    listener = thread.language.store(listener)
    print(listener.trd["ram"])


langTest(listener)

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


memTest(memBank)

# move testing
movObj = object.object("irrelevant", {"mov": [0, 0, 0, 1, 1, 1, 3, 4, 5]}, {"name": "movObj",
                                                                            "previous location": [0, 0, 0]})


def movTest(movObj):
    print(movObj.tag["previous location"])
    movObj = thread.move.warp(movObj, 3, 4, 5)
    print(movObj.trd["mov"])


# tread.move.moveto seems broken (in 3,4,5 out 3,3,3) fix it
movTest(movObj)


# If you think im going to test my joke phys module you are WRONG


# ram testing
ramStore = object.object("irrelevant", {"ram": []}, {"name": "ramStore"})
memBank = object.user("irreevant", {"ram": []}, "irrelevant", [0, ["start"], 2], {"name": "memBank",
                                                                                  "adminNote": "sorry"})


def ramTest(ramStore, memBank):
    ramStore = thread.ram.load(ramStore, "hi")
    ramStore = thread.ram.load(ramStore, "hi1")
    thread.ram.read(ramStore)
    ramStore = thread.ram.store(memBank, "store0", 0)
    print(memBank.mem)
    ramStore = thread.ram.free(ramStore, None)
    print(ramStore.trd["ram"])

ramTest(ramStore, memBank)

