# setup
# mov
#    x pos,y pos,z pos,x accel,y accel, z accel
#
# if obj is a sub obj mov will equal "sub"

class mov():
    def __init__(self, x, y, z, a, b, c):
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


# runtime
if __name__ == "__main__":
    print("move thread bolck v10.0")
