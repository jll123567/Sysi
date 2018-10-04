# This is a standard for labeling the changes functions make
# module type:std


# add the output tag
# obj(obj)*
# updatedObj(obj)
def addOutTags(obj):
    obj.tag.update({"out": ""})
    return obj


# set the output tag
# use the following or just do dta.tag["dataType"] = <string>
# obj(obj)*, output(str)*
# updatedObj(obj)
def setOut(obj, output):
    obj.tag["out"] = str(output)
    return obj


# remove the output tag
# obj(obj)
# updatedObj(obj)
def removeOutTags(obj):
    del obj.tag["dataType"]
    return obj


# output tags give info as to what a function will do as an array where each entry represents the output of a variable
# outs for ints
#   var = value
#   var + value
#   val - value
#   val * value
#   val / value
#   val ?(used when you know the function modifies val but not how
# outs for other types
#   var = value
#   var ?
# info at run
if __name__ == "__main__":
    print("This is a standard for labeling the changes functions make\nmodule type:std")
