# setup
def addOutTag(obj):
    obj.tag.update({"out": ""})
    return obj


# use the following or just do dta.tag["dataType"] = <string>
def setType(obj, outputs):
    obj.tag["out"] = str(outputs)
    return obj


def removeTypeTags(obj):
    obj.tag.pop("out")
    return obj
# how to use
# this tag is for thread creation @ Content Generation Engine(coming somepoint after this writing) @ sysh
# list the outputs of a function stored in data
# for ints
#   int=value
#   int + value
#   int - value
#   int * value
#   int / vlaue
#   int ? (used when the output type is known but not the value)
# for strings, bools, realy anything else
#   item = value
#   item ? (used when the output type is known but not the value)


#runtime
if __name__ == "__main__":
    print("out tag v10.0")
