# setup
class object:
    def __init__(self, mod, trd, tag):
        self.mod = mod
        # Check ./adminProg/model.py
        self.trd = trd
        self.tag = tag
        # required tags
        # name


class user:
    def __init__(self, mod, trd, prs, mem, tag):
        self.mod = mod
        self.tag = tag
        self.trd = trd
        self.prs = prs
        # working on it
        self.mem = mem
        # [internal,real,storeage]
        # [obj,obj,...]timesort

    # Recomended once a year
    def usershipQuery(obj):
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
                if isinstance(obj, user):
                    oldUsrDta = [obj.prs + obj.mem]
                    objActual = object(obj.mod, obj.trd, obj.tag)
                    obj.tag.update({"notes": oldUsrDta})
                    print(obj.tag["name"], "is Now Object")
                    return objActual
                else:
                    print(obj.tag["name"], "is Object")
        if not fail:
            if isinstance(obj, object):
                usr = user(obj.mod, obj.trd, obj.tag["notes"][0], obj.tag["notes"][1], obj.tag)
                print(obj.tag["name"], "is Now User")
                return usr
            else:
                print(obj.tag["name"], "is User")


class weapon:
    def __init__(self, mod, trd, dmg, tag):
        self.mod = mod
        self.tag = tag
        self.trd = trd
        self.dmg = dmg
        # damage profile


class data:
    def __init__(self, storage, tag):
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
