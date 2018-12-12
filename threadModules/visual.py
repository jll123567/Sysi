# visual data and camera handling
# module type: def


import object
# feed=[raw,pitch,yaw,roll]


class vis:
    def __init__(self, rawImg=None, pitch=0, yaw=0, roll=0):
        if rawImg is None:
            self.rawImg = []
        else:
            self.rawImg = rawImg
        self.rx = pitch
        self.ry = yaw
        self.rz = roll

    # set camera rotation
    # p(float)*, y(float)*, r(float)*
    # none
    def rotate(self, rx, ry, rz):
        self.rx = rx
        self.ry = ry
        self.rz = rz

    # clear image from raw img
    # none
    # none
    def clearImg(self):
        self.rawImg = []

    # reset position of camera
    # none
    # none
    def resetPos(self):
        self.rx = 0
        self.ry = 0
        self.rz = 0

    # pack data for ram
    # none
    # dta(vis attribs, tags)
    def package(self):
        return object.data([self.rawImg, self.rx, self.ry, self.rz], {"name": "tread.vis.package", "id": None,
                                                                      "dataType": "thread.vis.package"})


# info at run
if __name__ == "__main__":
    print("# visual data and camera handling\nmodule type: def")
