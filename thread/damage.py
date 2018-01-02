# import
from random import randint


# setup
# dmg
def phys(wep, obj):
    apl = wep.dmg[1] - obj.tag["stat"]["defence"]
    if apl < 0:
        apl = 0
    obj.tag["health"] -= apl
    return obj


def energy(wep, obj):
    dmg_set = False
    apl = 0
    for i in wep.dmg[2]:
        for f in obj.tag["stat"]["resist"]:
            if i == f[0]:
                apl = wep.dmg[1] - f[1]
                dmg_set = True
    if not dmg_set:
        apl = wep.dmg[1]
    if apl < 0:
        apl = 0
    obj.tag["health"] -= apl
    return obj


def internal(wep, obj):
    if "mem" in wep.dmg[2]:
        working = True
        while working:
            try:
                obj.mem[1].pop(randint(0, 9999999999))
            except:
                print("mem.remove fail /n retrying")
            else:
                working = False

    if "trd" in wep.dmg[2]:
        obj.trd["current"] = None
    else:
        print("unsupported")
    return obj


def stat(wep, obj):
    for i in obj.tag["stat"]:
        for f in wep.dmg[2]:
            if i == f:
                obj.tag["stat"][i] -= wep.dmg[1]
    return obj


def defend(wep, obj):
    obj.tag["health"] += wep.tag["stat"]["defence"]
    return obj


def attack(wep, obj):
    for _ in wep.dmg:
        print(obj.tag["health"])

        # runtime


if __name__ == "__main__":
    print("damage profile/attack handler v10.0")
