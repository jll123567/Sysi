# visual data and camera handleing
# module type: def
# feed=[raw,pitch,yaw,roll]


class vis:
    def __init__(self, rawImg=None, pitch=0, yaw=0, roll=0):
        if rawImg is None:
            self.rawImg = []
        else:
            self.rawImg = rawImg
        self.p = pitch
        self.y = yaw
        self.r = roll

    # set camera rotation
    # p(float)*, y(float)*, r(float)*
    # none
    def rotate(self, p, y, r):
        self.p = p
        self.y = y
        self.r = r

    # clear image from raw img
    # none
    # none
    def clearImg(self):
        self.rawImg = []

    # reset postion of camera
    # none
    # none
    def resetPos(self):
        self.p = 0
        self.y = 0
        self.r = 0


# info at run
if __name__ == "__main__":
    print("# visual data and camera handleing\nmodule type: def")
