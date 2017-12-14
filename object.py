#import

#setup
class object:
    def __init__(self, mod, trd, tag):
        self.mod = mod
        # {“block1”:[...],...}
        self.trd = trd
        # must have a name(“name”)
        # must have a location([cont,”x,y,z,p,ya,r”])
        self.tag = tag
        # necessary tags
        # name=all useable names
        # relevant_cont=smallest relevant container
        # uni=Host universs
        # id=“type”,”id (dervied from creation time)”
        # event_log=[log of events]
        # terms=guess


class user:
    def __init__(self, mod, trd, prs, mem, tag):
        self.mod = mod
        self.tag = tag
        self.trd = trd
        # working on it
        self.prs = prs
        # [internal,real,storeage]
        # [obj,obj,...]timesort
        self.mem = mem

    def get(var):
        return var

    # noinspection PyMethodFirstArgAssignment
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
        if not fail:
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
        # literaly fucking anything
        self.d = d


class container:
    def __init__(self, org, bnd, tag):
        # [supercont,x,y,z]
        self.org = org
        # [“(h/s)xyz-xyz”]
        self.bnd = bnd
        self.tag = tag


class scene:
    def __init__(self, scp, obj, loc, tag):
        # [time(time,tl branch),command0,command1,...]
        self.scp = scp
        # [obj0,obj1,...]
        self.obj = obj
        # cont
        # use a super cont that will contain all relevant containers
        self.loc = loc
        self.tag = tag


class universe:
    def __init__(self, tl, scn, obj, cont, funct, rule, tag):
        # time line(wip)
        self.tl = tl
        # scene list in order like(0,0)(0,1)(1,0)(1,1)
        self.scn = scn
        # objlist
        # [usr,wep,dev,obj,dta]
        self.obj = obj
        # containor struct
        self.cont = cont
        # functions unique to uni
        self.funct = funct
        # pisx and other functions to always run while in uni
        self.rule = rule
        # tags
        self.tag = tag
#    necesary tags
#        relevancy
#        name

#runtime
if __name__ == "__main__":
    print("object definitions v10.0")