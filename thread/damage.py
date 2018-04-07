# import
from random import randint

# wep.dmg = [[ammount (int), value to modify(string)], ...]


# a place holder for damage at the model, just stat dmg
def DEPRICATEDphysDEPRICATED(wep, obj):
    apl = wep.dmg[1] - obj.tag["stat"]["defence"]
    if apl < 0:
        apl = 0
    obj.tag["health"] -= apl
    return obj


# damages the internal of obj (mem type only on usr)
# Use: <obj> = Sysh.thread.damage.internal(<wep>, <obj>)
# Requires: obj, wep
def internal(wep, obj):
    for i in wep.dmg:
        if i[1] == "mem":
            working = True
            while working:
                try:
                    obj.mem[1].pop(randint(0, 9999999999))
                except IndexError:
                    print("mem.remove fail /n retrying")
                else:
                    working = False

        elif "trd" == i[1]:
            obj.trd["current"] = None
        else:
            print("unsupported")
    return obj


# modifies the value of <stat>
# Use: <obj> = Sysh.thread.damage.stat(<wep>, <obj>, <index of stat to modify>)
# Requires: obj, wep, matching stat in obj tags and dmg prof of wep
def stat(wep, obj, dmgIndex):
    for stat, val in obj.tag["stat"].iteritems():
        if obj.tag["stat"].stat == wep.dmg[dmgIndex][1]:
                obj.tag["stat"][stat] -= wep.dmg[0]
        else:
            print("obj does not have the stat ", wep.dmg[dmgIndex][1], " \nDid you mispell it?")
    return obj


# remove health based on atk
# Use: <obj> = Sysh.thread.damage.attack(<wep>, <obj>)
# Requires: obj wih health tag, wep with atk in prof
def attack(wep, obj):
    for i in wep.dmg:
        if i[1] == "atk":
            obj.tag["health"] -= i[0]
    return obj


# runtime
if __name__ == "__main__":
    print("damage profile/attack handler v10.0")
