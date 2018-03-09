# import
import thread.complex
import thread.damage
import object

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
punchingBag = object.object("irrelevant", "irrelevant", {"name": "punching bag", "stat": {"defence": 2}, "health": 100})


def dmgTst(dmgTest, punchingBag):
    print("init\n", punchingBag.tag["health"])
    punchingBag = thread.damage.attack(dmgTest, punchingBag)
    print("after hit(rough 82)\n", punchingBag.tag["health"])


dmgTst(dmgTest, punchingBag)
