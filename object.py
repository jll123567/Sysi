class object:
    def __init__(self, mod, trd, tag):
        self.mod = mod
        # model of object
        self.trd = trd
        # must have a move block w/ location([cont,"x,y,z,p,ya,r"])
        self.tag = tag
        # necessary tags for all objects
        # name=all usable names
        # relevant_cont=smallest relevant container
        # uni=Host universes
        # id="type","id (derived from creation time)"
        # event_log=[log of events]
        # terms=relevant terms


class user:
    def __init__(self, mod, trd, prs, mem, tag):
        self.mod = mod
        self.tag = tag
        self.trd = trd
        self.prs = prs
        self.mem = mem
        # [internal,real,storage]
        # [obj,obj,...]time sorted

    def get(var):
        return var

    def usershipQuery(obj):
        print("can get info from and modify $HostUni")
        rww = input("y/n")
        print("can get and store objects in memory")
        rwi = input("y/n")
        print("attempts to add reason to previous current and future actions")
        rea = input("y/n")
        print("can add new functions to tasker")
        lrn = input("y/n")
        print("does not == another obj")
        unq = input("y/n")
        total = [rww, rwi, rea, lrn, unq]
        fail = False
        for i in total:
            if i != 'y' or i != 'n':
                fail = True
                print("form incorrectly filled")
                break
            if i == 'n':
                fail = True
                if type(obj) == type(user(0, 0, 0, 0, 0)):
                    oldUsrDta = obj.prs + obj.mem
                    obj = object(obj.mod, obj.trd, obj.tag)
                    obj.tag["notes"] = oldUsrDta
                    print(obj.tag["name"], "is Now Object")
                else:
                    print(obj.tag["name"], "is Object")
        if fail == False:
            if type(obj) == object(0, 0, 0):
                obj = user(obj.mod, obj.trd, obj.tag["notes"][0], obj.tag["notes"][1], obj.tag)
                print(obj.tag["name"], "is Now User")
            else:
                print(obj.tag["name"], "is User")


class device:
    def __init__(self, mod, trd, tag):
        self.mod = mod
        self.tag = tag
        self.trd = trd


class weapon:
    def __init__(self, mod, trd, dmg, tag):
        self.mod = mod
        self.tag = tag
        self.trd = trd
        # damage profile
        self.dmg = dmg


class data:
    def __init__(self, d, tag):
        self.tag = tag
        # literally fucking anything
        self.d = d


class container:
    def __init__(self, org, bnd, tag):
        self.org = org
        # [supercont,x,y,z]
        self.bnd = bnd
        # ["(h/s)xyz-xyz"]
        self.tag = tag


class scene:
    def __init__(self, scp, obj, loc, tag):
        self.scp = scp
        # [time(time,tl branch),command0,command1,...]
        self.obj = obj
        # [obj0,obj1,...]
        self.loc = loc
        # cont
        # use a super cont that will contain all relevant containers
        self.tag = tag


class universe:
    def __init__(self, tl, scn, obj, cont, funct, rule, tag):
        self.tl = tl
        # time line
        self.scn = scn
        # scene list in order like(0,0)(0,1)(1,0)(1,1)
        self.obj = obj
        # object list
        # [obj,usr,dev,wep,dta]
        self.cont = cont
        # container structure
        self.funct = funct
        # functions unique to uni
        self.rule = rule
        # phisx and other functions to always run while in uni
        self.tag = tag

    # necessary tags
    # relevancy
    # name

    # runtime


if __name__ == "__main__":
    print("object definitions v10.0")

    # Made by Jacob Ledbetter
