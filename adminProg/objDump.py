# setup
def dump_parser(content, indent):
    if not isinstance(content, list) and not isinstance(content, dict):
        print(str(content))
    else:
        for i in content:
            if isinstance(i, list) or isinstance(i, dict):
                dump_parser(i, indent + 1)
            else:
                print(("  " * indent) + str(i))


def udump(usr):
    try:
        print(usr.tag["name"])
        print(" memory")
        dump_parser(usr.mem[1], 1)
        dump_parser(usr.mem[2], 1)
        print(" model")
        dump_parser(usr.mod, 1)
        print(" ram")
        dump_parser(usr.trd["ram"], 1)
        print(" visual")
        dump_parser(usr.trd["vis"], 1)
        print(" model")
        print("  ", usr.tag["container"])
        dump_parser(usr.trd["mov"], 1)
        print(" language")
        dump_parser(usr.trd["lang"], 1)
        print(" complex")
        dump_parser(usr.trd["cpx"], 1)
        print(" queue")
        dump_parser(usr.trd["que"], 1)
        print(" tasker profiles")
        dump_parser(usr.trd["tsk"], 1)
        print(" pers")
        dump_parser(usr.pers, 1)
    except:
        print("not a valid user,no name or container specified, or user is too large")


def odump(obj):
    try:
        print(obj.tag["name"])
        print(" model")
        dump_parser(obj.mod, 1)
        print(" thread")
        for i in obj.trd:
            print("  ", obj.trd.index(i))
            dump_parser(i, 2)
    except:
        print("object is either invalid, not named, or too large")


def wdump(wep):
    try:
        print(wep.tag["name"])
        print(" model")
        dump_parser(wep.mod, 1)
        print(" thread")
        for i in wep.trd:
            print("  ", wep.trd.index(i))
            dump_parser(i, 2)
        print(" damage profile")
        dump_parser(wep.dmg, 1)
    except:
        print("wep is either invalid, not named, or too large")


def dtdump(dta):
    try:
        print(dta.tag["name"])
        print(" data")
        dump_parser(dta.storage, 1)
    except:
        print("data is either invalid, not named, or too large")


def cdump(cont):
    try:
        print(cont.tag["name"])
        print(" origin")
        dump_parser(cont.org, 1)
        print(" bounds")
        dump_parser(cont.bnd, 1)
    except:
        print("container is either invalid, not named, or too large")


def sdump(scn):
    try:
        print(scn.tag["name"])
        print(" script")
        dump_parser(scn.scp, 1)
        print(" sub-objects")
        dump_parser(scn.obj, 1)
        print(" relevant container")
        dump_parser(scn.loc, 1)
    except:
        print("scene is either invalid, not named, or too large")


# runtime
if __name__ == "__main__":
    print("dumpualization functions v10.0")
