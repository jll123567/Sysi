# setup

# model stores model of the object
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


class sysModel:
    #
    def __init__(self, geom=None, skel=None, ani=None, mat=None):
        if geom is None:
            self.geom = {"scale": 1, "lines": ["0,0,0-0,0,0"]}
        else:
            self.geom = geom
        if skel is None:
            self.skel = {"scale": 1, "points": ["0,0,0", ["0,0,0"]]}
        else:
            self.skel = skel
        if ani is None:
            self.ani = {"default": {"scale": 1, "animation": [["0,0,0", "0,0,0", ]]}}
        else:
            self.ani = ani
        if mat is None:
            self.mat = {"texture": None, "physx": [None]}
        else:
            self.mat = mat

    def addAnimation(self, animation):
        self.ani.update(animation)

    def changeMaterial(self, texture, physx):
        self.mat["texture"] = texture
        self.mat["physx"] = physx


class fileModel:
    def __init__(self, file):
        self.file = file


# runtime
if __name__ == "__main__":
    print("model rigging v11.0")
