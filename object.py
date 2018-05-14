# import
from random import randint
import atribs.thread
import atribs.model
import atribs.damage
import atribs.memory
import atribs.personality


# setup
class object:
    def __init__(self, mod=atribs.model.sysModel(), trd=atribs.thread.trd(), tag={"name": None}):
        self.mod = mod
        self.trd = trd
        self.tag = tag
        # required tags
        # name

    def makeModelAssembly(self):
        oldModel = self.mod
        # noinspection PyTypeChecker
        self.tag.update({"oldModel": oldModel})
        self.mod = "assem"

    # damages the internal of obj (mem type only on usr)
    # Use: usr.Sysh.object.internal(<wep>)
    # Requires: usr|obj, wep
    def internalDamage(self, wep):
        for i in wep.dmg.damages:
            if i[1] == "mem":
                working = True
                while working:
                    # noinspection PyBroadException
                    try:
                        self.mem.real.pop(randint(0, 9999999999))
                    except IndexError:
                        print("mem.remove fail /n retrying")
                    except:
                        print("unknown error, is this a user?")
                    else:
                        working = False

            elif "trd" == i[1]:
                self.trd.tsk.current = None
            else:
                print("unsupported")

    # modifies the value of <stat>
    # Use: obj.Sysh.thread.damage.stat(<wep>, <index of stat to modify>)
    # Requires: obj, wep, matching stat in obj tags and dmg profile of wep
    def statDamage(self, wep, dmgIndex):
        for key in self.tag["stat"].keys():
            if key == wep.dmg.damages[dmgIndex][1]:
                self.tag["stat"][key] -= wep.dmg[dmgIndex][0]
            else:
                print("obj does not have the stat ", wep.dmg[dmgIndex][1], " \nDid you mispell it?")

    # remove health based on atk
    # Use: obj.Sysh.thread.damage.attack(<wep>)
    # Requires: obj wih health tag, wep with health in prof
    def attack(self, wep):
        for i in wep.dmg.damages:
            if i[1] == "health":
                self.tag["health"] -= i[0]

    # Recomended once a year
    def usershipQuery(self):
        print("can get info from and modify $HostUni")
        rww = input("y/n")
        print("can get and store objects in memory")
        rwi = input("y/n")
        print("attempts to add reason to previous current and future actions")
        rea = input("y/n")
        print("can add new functions to tasker")
        lrn = input("y/n")
        print("attempts to reserve or increase the intregrity and freewill of objects or users")
        mor = input("y/n")
        print("does not == another obj")
        unq = input("y/n")
        total = [rww, rwi, rea, lrn, unq, mor]
        fail = False
        for i in total:
            if i != 'y' or i != 'n':
                fail = True
                print("form incorrectly filled")
                break
            if i == 'n':
                fail = True
                if isinstance(self, user):
                    oldUsrDta = [self.prs, self.mem]
                    objActual = object(self.mod, self.trd, self.tag)
                    # noinspection PyTypeChecker
                    self.tag.update({"oldUsrDta": oldUsrDta})
                    print(self.tag["name"], "is Now Object")
                    return objActual
                else:
                    print(self.tag["name"], "is Object")
        if not fail:
            if isinstance(self, object):
                usr = user(self.mod, self.trd, self.tag["notes"][0], self.tag["notes"][1], self.tag)
                print(self.tag["name"], "is Now User")
                return usr
            else:
                print(self.tag["name"], "is User")


class user(object):
    def __init__(self, mod=atribs.model.sysModel(), trd=atribs.thread.trd(), prs=atribs.personality.prs(),
                 mem=atribs.memory.mem(), tag={"name": None}):
        self.mod = mod
        self.tag = tag
        self.trd = trd
        self.prs = prs
        # working on it
        self.mem = mem
        # [internal,real,storeage]
        # [obj,obj,...]timesort

    # saves a copy of ram ro memory
    # use: <usr> = Sysh.thread.ram.store(<usr>, <string>, <int between 0 and 100>)
    # requires: usr
    def storeToMemory(self, storedRamName, storedRamImportance):
        dta = data([self.trd.ram.storage], {"name": storedRamName, "relevancy": [0, 0, storedRamImportance]})
        self.mem.store(1, dta)

    def loadToRam(self, block, index):
        if block == 0:
            print("no internal access")
        elif block == 1:
            self.trd.ram.load(self.mem.real[index])
        else:
            self.trd.ram.load(self.mem.external[index])


class weapon(object):
    def __init__(self, mod=atribs.model.sysModel(), trd=atribs.thread.trd(),
                 dmg=atribs.damage.dmg(), tag={"name": None}):
        self.mod = mod
        self.tag = tag
        self.trd = trd
        self.dmg = dmg
        # damage profile


class data:
    def __init__(self, storage=None, tag={"name": None}):
        self.tag = tag
        self.storage = storage
        # anything you want to store


class container:
    def __init__(self, org, bnd, tag):
        self.org = org
        # [supercont,x,y,z]
        # if is largest cont do None
        self.bnd = bnd
        # [“(h/s)x,y,z-x,y,z”]
        self.tag = tag


class scene:
    def __init__(self, scp, obj, loc, tag):
        self.scp = scp
        # [time(time,tl branch),command0,command1,...]
        self.obj = obj
        # objlist
        # [usr, wep, obj, dta]
        # ["obj0=object.w/e(s,t,u,f,f)", ...]
        self.loc = loc
        # cont
        # use a super cont that will contain all relevant containers
        self.tag = tag


class universe:
    def __init__(self, tl, scn, obj, cont, funct, rule, tag):
        self.tl = tl
        # time line(wip)
        self.scn = scn
        # scene list in or
        # der like(0,0)(0,1)(1,0)(1,1)
        self.obj = obj
        # objlist
        # [usr, wep, obj, dta]
        # ["obj0=object.w/e(s,t,u,f,f)", ...]
        self.cont = cont
        # container struct
        self.funct = funct
        # functions unique to uni
        self.rule = rule
        # phisx and other functions to always run while in uni
        self.tag = tag


# runtime
if __name__ == "__main__":
    print("object definitions v10.0")
