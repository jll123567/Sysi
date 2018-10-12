# movement and position tracking
# module type: def
# mov
#    x pos,y pos,z pos,x accel,y accel, z accel
#
# if obj is a sub obj mov will equal "sub"


# thread module for position and movement
# x pos(float)*, y pos(float)*, z pos(float)*, x accel(float)*, y accel(float)*, z accel(float)*
class mov:
    def __init__(self, x=0, y=0, z=0, a=0, b=0, c=0):
        self.x = x
        self.y = y
        self.z = z
        self.a = a
        self.b = b
        self.c = c

    # sets obj's position in the threadModules
    # x(float)*, y(float)*, z(float)*
    # none
    def warp(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    # sets object acceleration in threadModules
    # x accel(float)*, y accel(float)*, z accel(float)*
    # none
    def accelerate(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    # moves obj based on acceleration
    # none
    # none
    def move(self):
        self.x += self.a
        self.y += self.b
        self.z += self.c

    # accelerates this obj based on a force and an obj's mov
    # o1(mov)*, force(float)*
    # none
    def attract(self, o1, force):
        if self.x > o1.x:
            self.a = (force * -1)
        elif self.x < o1.x:
            self.a = force
        else:
            self.a = 0
        if self.y > o1.y:
            self.b = (force * -1)
        elif self.y < o1.y:
            self.b = force
        else:
            self.b = 0
        if self.z > o1.z:
            self.c = (force * -1)
        elif self.z < o1.z:
            self.c = force
        else:
            self.c = 0
        self.move()

    # accelerates this obj based on a force and an obj's mov
    # o1(mov)*, force(float)*
    # none
    def repel(self, o1, force):
        if self.x > o1.x:
            self.a = force
        elif self.x < o1.x:
            self.a = force * -1
        else:
            self.a = 0
        if self.y > o1.y:
            self.b = force
        elif self.y < o1.y:
            self.b = force * -1
        else:
            self.b = 0
        if self.z > o1.z:
            self.c = force
        elif self.z < o1.z:
            self.c = force * -1
        else:
            self.c = 0
        self.move()


# Info at run
if __name__ == "__main__":
    print("movement and position tracking\nmodule type: def")
