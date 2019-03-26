"""Definition for obj.mod.
    Model stores what an sysObject looks like.
"""


class sysModel:
    """sysh's own 3d model format(why not?)"""

    def __init__(self, geom=None, skel=None, ani=None):
        """geom: {"scale": int, "points": ["x,y,z-x,y,z","more points"]}
            skel: {"scale": int, "points": [skeleton point"x,y,z",["points bound to it(by offset)"x,y,z","..."], [...]}
            ani: {animationName: {"scale": int, [[original skpos"x,y,z", new pos(1ms later)"x,y,z", "..."], [...]]},
                nextAnimation: [...]}
            Note that parents have a model of "assem".
        """
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

    def addAnimation(self, animation):
        """Add a new animation to the model."""
        self.ani.update(animation)


class fileModel:
    """Model based on a file."""
    def __init__(self, file):
        """File: any"""
        self.file = file
