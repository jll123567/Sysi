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
# note: parts of assemblies {"scale": int,["x,y,z,pitch,yaw,roll",obj]} with "material": "assem"


def makeModel(obj, model, material):
    obj.mod["geometry"] = model
    obj.mod["material"] = material
    return obj
#    else:
#        points=[[]]
#        working=True
#        while working:
#            if points=[[]]:
#                points.insert(0,input("scale from a(1mm=100000000a so 100000000)"))
#            x1=0
#            y1=0
#            z1=0
#            print("first point of new edge from origin")
#            x1=input("x:")
#            y1=input("y:")
#            z1=input("z:")
#            x2=0
#            y2=0
#            z2=0
#            print("second point of new edge from origin")
#            x2=input("x:")
#            y2=input("y:")
#            z2=input("z:")
#            points[1].append(str(str(x1)+","+str(y1)+","+str(z1)+"-"str(x2)+","str(y2)+","str(z2))
#            check=input("are you done(y/n)")
#            if check="y":
#                working=False
#        object.mod[0]=points


def rigModel(obj, skeleton):
    obj.mod["skeleton"] = skeleton
    return obj


def setAnimations(obj, ani):
    obj.mod["animations"] = ani
    return obj


def addAnimation(obj, animation):
    obj.mod["animations"].update(animation)
    return obj


"""def displaySysModel(obj):
    print("scale:" + obj.mod["geometry"]["scale"] + "global units for one unit of this model")
    for f in obj.mod["geometry"]["points"]:
        if isinstance(f, list):
            displaySysModel(f[1])
            print("@" + f[0])
        else:
            print(f)
    print(obj.mod["skeleton"]["scale"])
    for i in obj.mod["skeleton"]["points"]:
        print(i)
    print(obj.mod[2][0], "frames per second")
    for i in obj.mod[2][1]:
        print(i)
    print("material:", obj.mod[3])


def newAssem(obj, assem, ani, rig):
    obj.mod["geometry"] = assem
    obj.mod["skeleton"] = rig
    obj.mod[""] = ani
    obj.mod[3] = "assem"
    return obj

    # open("filename","mode")"""


def imgAsModel(obj, file):
    obj.mod = file
    return obj


def stlAsModel(obj, file):
    obj.mod = file
    return obj


# runtime
if __name__ == "__main__":
    print("model rigging v10.0")
