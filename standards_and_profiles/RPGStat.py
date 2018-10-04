# adds some simple stats from most role playing games.
# hp not needed as it part of obj
# module type: std


# add the stat tag
# obj(obj)*
# updatedObj(obj)
def addTags(obj):
    obj.tag.update({"stat": {"atk": 0, "def": 0, "agi": 0, "int": 0}})
    return obj


# modify the stat tag
# obj(obj)*, atk(int)*, defence(int)*, agi(agi)*, intelligence(int)
# updatedObj(obj)
def modifyTags(obj, atk, defence, agi, intl):
    obj.tag["stat"]["atk"] = atk
    obj.tag["stat"]["def"] = defence
    obj.tag["stat"]["agi"] = agi
    obj.tag["stat"]["int"] = intl
    return obj


# remove the stat tag
# obj(obj)*
# updatedObj(obj)
def removeTags(obj):
    del obj.tag["stat"]["atk"]
    del obj.tag["stat"]["def"]
    del obj.tag["stat"]["agi"]
    del obj.tag["stat"]["int"]
    return obj


# info at run
if __name__ == "__main__":
    print("adds some simple stats from most role playing games.\nhp not needed as it part of obj\nmodule type: std")
