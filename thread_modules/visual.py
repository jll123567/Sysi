"""visual data and camera handling"""
import object


class vis:
    """hold and process visual data

    rawImg is a list with images(images will be added later)
    rx is float representing degrees
    so are ry and rz"""
    def __init__(self, rawImg=None, pitch=0, yaw=0, roll=0):
        """initialize sysObject attributes
        rawImg is an empty list
        pitch is 0
        yaw is 0
        roll is 0"""
        if rawImg is None:
            self.rawImg = []
        else:
            self.rawImg = rawImg
        self.rx = pitch
        self.ry = yaw
        self.rz = roll

    def rotate(self, rx, ry, rz):
        """set the rotation attributes of the visual thread"""
        self.rx = rx
        self.ry = ry
        self.rz = rz

    # clear image from raw img
    # none
    # none
    def clearImg(self):
        """set the rawImg attribute to an empty list"""
        self.rawImg = []

    # reset position of camera
    # none
    # none
    def resetPos(self):
        """set rotation attributes to 0"""
        self.rx = 0
        self.ry = 0
        self.rz = 0

    # pack data for ram
    # none
    # dta(vis attribs, tags)
    def package(self):
        """pack attributes into a data sysObject and return it"""
        return object.data([self.rawImg, self.rx, self.ry, self.rz], {"name": "tread.vis.package", "id": None,
                                                                      "dataType": "thread.vis.package"})


# info at run
if __name__ == "__main__":
    print("# visual data and camera handling\nmodule type: def")
