# Definition for obj.mod
# module type:def
# model stores what an object looks like
# accepts png, stl, and the method below
#
# Model format:
#
# {"geometry": {"scale": int, "points": ["x,y,z-x,y,z","more points"]},
# "skeleton": {"scale": int, "points": [skeleton point"x,y,z",["points bound to it(by offset)"x,y,z","..."], [...]},
# "animations": {animationName: {"scale": int, [[original skpos"x,y,z", new pos(1ms later)"x,y,z", "..."], [...]]},
#       nextAnimation: [...]},
# "material": {"texture": "./a_png_or something.jpeg", "physx": [physx properties(wip)]}
# note: parents have a model of "assem"(str)


# sysh's own 3d model format
# geom(model Geometry), skel(model skeleton points), ani(animations), mat(material definitions)
class sysModel:
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

    # adds a new animation to the model
    # animation(sysModel animation)*
    # none
    def addAnimation(self, animation):
        self.ani.update(animation)

    # changes the model's material to the listed one
    # texture(surface texture)*, physx(material physics)*
    # none
    def changeMaterial(self, texture, physx):
        self.mat["texture"] = texture
        self.mat["physx"] = physx


# a model based on a file
# file(a file)*
class fileModel:
    def __init__(self, file):
        self.file = file


# info at run
if __name__ == "__main__":
    print("Definition for obj.mod\nmodule type:def")
