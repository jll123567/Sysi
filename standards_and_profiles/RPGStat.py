# adds some simple stats from most role playing games.
# hp not needed as it part of obj
# module type: std


def addTags(obj):
    """Add atk, def, agi, int, to tag["stat"]."""
    obj.tag["stat"].update({"atk": 0, "def": 0, "agi": 0, "int": 0})
    return obj


def modifyTags(obj, atk, defence, agi, intl):
    """Modify the stat tags atk, def, agi, and int."""
    obj.tag["stat"]["atk"] = atk
    obj.tag["stat"]["def"] = defence
    obj.tag["stat"]["agi"] = agi
    obj.tag["stat"]["int"] = intl
    return obj
