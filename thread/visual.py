# setup
# visual
# feed=[raw,pitch,yaw,roll,[obj]]


class vis:
    def __init__(self, rawImg=None, pitch=0, yaw=0, roll=0, idObj=None):
        if rawImg is None:
            self.rawImg = []
        else:
            self.rawImg = rawImg
        self.p = pitch
        self.y = yaw
        self.r = roll
        if idObj is None:
            self.idObj = []
        else:
            self.idObj = idObj

    # set camera rotation
    # use: <obj> = rotate(<obj>, <int representing pitch>, <int representing yaw>, <int representing roll>)
    # requires: obj
    def rotate(self, p, y, r):
        self.p = p
        self.y = y
        self.r = r

    # obj ID at some point

    def clearImg(self):
        self.rawImg = []

    def clearId(self):
        self.idObj = []

    def resetPos(self):
        self.p = 0
        self.y = 0
        self.r = 0


# runtime
if __name__ == "__main__":
    print("visuals v11.0")
