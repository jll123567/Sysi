# setup
# mov
#    x pos,y pos,z pos,x accel,y accel, z accel
#
# if obj is a sub obj mov will equal "sub"


class mov():
    def __init__(self, x=0, y=0, z=0, a=0, b=0, c=0):
        self.x = x
        self.y = y
        self.z = z
        self.a = a
        self.b = b
        self.c = c

    # sets obj's position in the thread
    # use: <obj> = Sysh.thread.move.warp(<obj>, <int/float>, <int/float>, <int/float>)
    # requires: obj
    def warp(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    # sets object acceleration in thread
    # use: <obj> = Sysh.thread.move.accelerate(<obj>, <int/float>, <int/float>, <int/float>)
    # requires: obj
    def accelerate(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    # moves obj based on acceleration
    # use: <obj> = Sysh.thread.move.move(<obj>)
    # requires: obj
    def move(self):
        self.x += self.a
        self.y += self.b
        self.z += self.c

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


# runtime
if __name__ == "__main__":
    print("move thread bolck v10.0")
