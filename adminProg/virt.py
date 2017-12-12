import object


def virt_parser(content, indent):
    if type(content) != type([""]) and type(content) != type({"": ""}):
        print(str(content))
    else:
        for i in content:
            if type(i) == type([""]) or type(i) == type({"": ""}):
                virt_parser(i, indent + 1)
            else:
                print(("  " * indent) + str(i))


def uvirt(usr):
    try:
        print(usr.tag["name"])
        print(" memory")
        virt_parser(usr.mem[1], 1)
        virt_parser(usr.mem[2], 1)
        print(" model")
        virt_parser(usr.mod, 1)
        print(" ram")
        virt_parser(usr.trd["ram"], 1)
        print(" visual")
        virt_parser(usr.trd["vis"], 1)
        print(" model")
        print("  ", usr.tag["container"])
        virt_parser(usr.trd["mov"], 1)
        print(" language")
        virt_parser(usr.trd["lang"], 1)
        print(" complex")
        virt_parser(usr.trd["cpx"], 1)
        print(" queue")
        virt_parser(usr.trd["que"], 1)
        print(" tasker profiles")
        virt_parser(usr.trd["tsk"], 1)
        print(" pers")
        virt_parser(usr.pers, 1)
    except:
        print("not a valid user,no name or container specified, or user is too large")


def ovirt(obj):
    try:
        print(obj.tag["name"])
        print(" model")
        virt_parser(obj.mod, 1)
        print(" thread")
        for i in obj.trd:
            print("  ",obj.trd.index(i))
            virt_parser(i, 2)
    except:
        print("object is either invalid, not named, or too large")


def dvirt(dev):
    try:
        print(dev.tag["name"])
        print(" model")
        virt_parser(dev.mod, 1)
        print(" thread")
        for i in dev.trd:
            print("  ",dev.trd.index(i))
            virt_parser(i, 2)
    except:
        print("device is either invalid, not named, or too large")


def wvirt(wep):
    try:
        print(wep.tag["name"])
        print(" model")
        virt_parser(wep.mod, 1)
        print(" thread")
        for i in wep.trd:
            print("  ",wep.trd.index(i))
            virt_parser(i, 2)
        print(" damage profile")
        virt_parser(wep.dmg, 1)
    except:
        print("wep is either invalid, not named, or too large")


def dtvirt(dta):
    try:
        print(dta.tag["name"])
        print(" data")
        virt_parser(dta.d, 1)
    except:
        print("data is either invalid, not named, or too large")


def cvirt(cont):
    try:
        print(cont.tag["name"])
        print(" origin")
        virt_parser(cont.org, 1)
        print(" bounds")
        virt_parser(cont.bnd, 1)
    except:
        print("container is either invalid, not named, or too large")


def svirt(scn):
    try:
        print(scn.tag["name"])
        print(" script")
        virt_parser(scn.scp, 1)
        print(" sub-objects")
        virt_parser(scn.obj, 1)
        print(" relevant container")
        virt_parser(scn.loc, 1)
    except:
        print("scene is either invalid, not named, or too large")

        # runtime


if __name__ == "__main__":
    print("virtualization functions v10.0")


# by jacob ledbetter
