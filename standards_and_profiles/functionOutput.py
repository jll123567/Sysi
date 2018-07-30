##ADMIN TOOL##
# setup
def addOutTags(obj):
    obj.tag.update({"out": ""})
    return obj


# use the following or just do dta.tag["dataType"] = <string>
def setOut(obj, output):
    obj.tag["out"] = str(output)
    return obj


def removeOutTags(obj):
    del obj.tag["dataType"]
    return obj


# output tags give info as to what a fucntion will do as an array where each entry represents the output of a variable
# outs for ints
#   var = value
#   var + value
#   val - value
#   val * value
#   val / value
#   val ?(used when you know the function modifies but not how
# outs for other types
#   var = vlaue
#   var ?
# runtime
if __name__ == "__main__":
    print("output tags v11.0")
