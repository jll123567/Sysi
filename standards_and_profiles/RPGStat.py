##ADMIN TOOL##
# setup
# adds some simple stats from most role playing games, because I am a nerd.
# hp not needed as it part of wep


def addTags(obj):
    obj.tag.update({"stat": {"atk": 0, "def": 0, "agi": 0, "lck": 0}})
    return obj


def modifyTags(obj, atk, defence, agi, lck):
    obj.tag["atk"] = atk
    obj.tag["def"] = defence
    obj.tag["agi"] = agi
    obj.tag["lck"] = lck
    return obj


def removeTags(obj):
    del obj.tag["atk"]
    del obj.tag["def"]
    del obj.tag["agi"]
    del obj.tag["lck"]
    return obj


# runtime
if __name__ == "__main__":
    print("RPG stats v11.0")
