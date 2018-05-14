# wep.dmg = [[ammount (int), value to modify(string)], ...]
class dmg:
    def __init__(self, damages={"health": 0}):
        self.damages = damages


# a place holder for damage at the model, just stat dmg
def DEPRICATEDphysDEPRICATED(wep, obj):
    apl = wep.dmg[1] - obj.tag["stat"]["defence"]
    if apl < 0:
        apl = 0
    obj.tag["health"] -= apl
    return obj


# runtime
if __name__ == "__main__":
    print("damage profile/attack handler v10.0")
