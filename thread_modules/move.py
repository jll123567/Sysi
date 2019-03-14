"""movement and position tracking"""
import sys_objects


class mov:
    """holds sysObject position, acceleration and rotation"""
    def __init__(self, x=0, y=0, z=0, vx=0, vy=0, vz=0, rx=0, ry=0, rz=0, rvx=0, rvy=0, rvz=0):
        """initialize attributes

        x: x position
        y: y position
        z: z position
        vx: x velocity
        vy: y velocity
        vz: z velocity
        rx: pitch
        ry: yaw
        rz: roll
        rvx: pitch velocity
        rvy: yaw velocity
        rvz: roll velocity"""
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

    def warp(self, x, y, z):
        """set position"""
        self.x = x
        self.y = y
        self.z = z
    
    def setRotation(self, rx, ry, rz):
        """set rotation(degrees)"""
        self.rx = rx
        self.ry = ry
        self.rz = rz

    def accelerate(self, vx, vy, vz):
        """set acceleration"""
        self.vx = vx
        self.vy = vy
        self.vz = vz

    def accelerateRotation(self, rvx, rvy, rvz):
        """set rotation acceleration"""
        self.rvx = rvx
        self.rvy = rvy
        self.rvz = rvz

    def move(self):
        """change position and rotation based on acceleration"""
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz
        self.rx += self.rvx
        self.ry += self.rvy
        self.rz += self.rvz

    def attract(self, o1, force):
        """changes position based on another sysObject's position and a force

        o1 needs to be a trd.mov not an sysObject.sysObject
        attract pusses together"""
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

    def repel(self, o1, force):
        """changes position based on another sysObject's position and a force

        o1 needs to be a trd.mov not an sysObject.sysObject
        repel pushes away"""
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

    def package(self):
        """pack attributes into a data sysObject and return it"""
        return sys_objects.data([self.x, self.y, self.z, self.vx, self.vy, self.vz, self.rx,
                                 self.ry, self.rz, self.rvx, self.rvy, self.rvz],
                                {"name": "tread.mov.package", "id": None, "dataType": "thread.mov.package"})
