# movement and position tracking
# module type: def
# mov
#    x pos,y pos,z pos,x accel,y accel, z accel
#
# if obj is a sub obj mov will equal "sub"
import object


# thread module for position and movement
# x pos(float)*, y pos(float)*, z pos(float)*, x accel(float)*, y accel(float)*, z accel(float)*
class mov:
    def __init__(self, x=0, y=0, z=0, vx=0, vy=0, vz=0, rx=0, ry=0, rz=0, rvx=0, rvy=0, rvz=0):
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx
        self.vy = vy
        self.vz = vz
        self.rx = rx
        self.ry = ry
        self.rz = rz
        self.rvx = rvx
        self.rvy = rvy
        self.rvz = rvz

    # sets obj's position in the threadModules
    # x(float)*, y(float)*, z(float)*
    # none
    def warp(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    # set the rotation of the object in radians
    # rx(float)*, ry(float)*, rz(float)*
    # none
    def setRotation(self, rx, ry, rz):
        self.rx = rx
        self.ry = ry
        self.rz = rz

    # sets object acceleration in threadModules
    # x accel(float)*, y accel(float)*, z accel(float)*
    # none
    def accelerate(self, vx, vy, vz):
        self.vx = vx
        self.vy = vy
        self.vz = vz

    # set the rotational velocity of the object(radians per shift)
    # rvx(float)*, rvy(float)*, rvz(float)*
    # none
    def accelerateRotation(self, rvx, rvy, rvz):
        self.rvx = rvx
        self.rvy = rvy
        self.rvz = rvz

    # moves obj based on acceleration
    # none
    # none
    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz
        self.rx += self.rvx
        self.ry += self.rvy
        self.rz += self.rvz

    # accelerates this obj based on a force and an obj's mov
    # o1(mov)*, force(float)*
    # none
    def attract(self, o1, force):
        if self.x > o1.x:
            self.vx = (force * -1)
        elif self.x < o1.x:
            self.vx = force
        else:
            self.vx = 0
        if self.y > o1.y:
            self.vy = (force * -1)
        elif self.y < o1.y:
            self.vy = force
        else:
            self.vy = 0
        if self.z > o1.z:
            self.vz = (force * -1)
        elif self.z < o1.z:
            self.vz = force
        else:
            self.vz = 0
        self.move()

    # accelerates this obj based on a force and an obj's mov
    # o1(mov)*, force(float)*
    # none
    def repel(self, o1, force):
        if self.x > o1.x:
            self.vx = force
        elif self.x < o1.x:
            self.vx = force * -1
        else:
            self.vx = 0
        if self.y > o1.y:
            self.vy = force
        elif self.y < o1.y:
            self.vy = force * -1
        else:
            self.vy = 0
        if self.z > o1.z:
            self.vz = force
        elif self.z < o1.z:
            self.vz = force * -1
        else:
            self.vz = 0
        self.move()

    # pack data for ram
    # none
    # dta(mov attribs, tags)
    def package(self):
        return object.data([self.x, self.y, self.z, self.vx, self.vy, self.vz, self.rx,
                            self.ry, self.rz, self.rvx, self.rvy, self.rvz],
                           {"name": "tread.mov.package", "id": None, "dataType": "thread.mov.package"})


# Info at run
if __name__ == "__main__":
    print("movement and position tracking\nmodule type: def")
