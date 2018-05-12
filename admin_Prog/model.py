# setup

# model stores any sort of model of the object
# accepts png, stl, and the method below
#
# Model format:
#
# {"geometry": {"scale": int, "points": ["x,y,z-x,y,z","more points"]},
# "skeleton": {"scale": int, "points": [skeleton point"x,y,z",["points bound to it(by offset)"x,y,z","..."], [...]},
# "animations": {animationName: {"scale": int, [[original skpos"x,y,z", new pos(1ms later)"x,y,z", "..."], [...]]},
#       nextAnimation: [...]},
# "material": {"texture": "./a_png_or something.jpeg", "physx": [physx properties(wip)]}
# note: parents have a model of "assem"


def makeModel(obj, model, material):
    obj.mod["geometry"] = model
    obj.mod["material"] = material
    return obj


def rigModel(obj, skeleton):
    obj.mod["skeleton"] = skeleton
    return obj


def setAnimations(obj, ani):
    obj.mod["animations"] = ani
    return obj


def addAnimation(obj, animation):
    obj.mod["animations"].update(animation)
    return obj


def makeAssembly(obj):
    obj.tag.update({"oldModel": obj.mod})
    obj.mod = "assem"
    return obj


def imgAsModel(obj, file):
    obj.mod = file
    return obj


def stlAsModel(obj, file):
    obj.mod = file
    return obj


# runtime
if __name__ == "__main__":
    print("model rigging v10.0")
