# setup

# model stores any sort of model of the selfect
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


class sysModel():
    def __init__(self, geom={"scale": 1, "lines": ["0,0,0-0,0,0"]},
                 skel={"scale": 1, "points": ["0,0,0", ["0,0,0"]]},
                 ani={"default": {"scale": 1, "animation": [["0,0,0", "0,0,0", ]]}},
                 mat={"texture": None, "physx": [None]}):
        self.geom = geom
        self.skel = skel
        self.ani = ani
        self.mat = mat

    def addAnimation(self, animation):
        self.ani.update(animation)

class fileModel():
    def __init__(self, file):
        self.file = file


# runtime
if __name__ == "__main__":
    print("model rigging v10.0")
