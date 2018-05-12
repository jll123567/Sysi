import thread.Thread
# setup
# mov
#    [x pos,y pos,z pos,x accel,y accel, z accel]
#
# if obj is a sub obj mov will equal "sub"

class mov(thread.Thread):
    def __init__(self, self.mov):

# sets obj's position in the thread
# use: <obj> = Sysh.thread.move.warp(<obj>, <int/float>, <int/float>, <int/float>)
# requires: obj
def warp(obj, x, y, z):
    obj.trd["mov"][0] = x
    obj.trd["mov"][1] = y
    obj.trd["mov"][2] = z
    return obj


# sets object acceleration in thread
# use: <obj> = Sysh.thread.move.accelerate(<obj>, <int/float>, <int/float>, <int/float>)
# requires: obj
def accelerate(obj, x, y, z):
    obj.trd["mov"][3] = x
    obj.trd["mov"][4] = y
    obj.trd["mov"][5] = z
    return obj


# moves obj based on acceleration
# use: <obj> = Sysh.thread.move.move(<obj>)
# requires: obj
def move(obj):
    obj.trd["mov"][0] += obj.trd["mov"][3]
    obj.trd["mov"][1] += obj.trd["mov"][4]
    obj.trd["mov"][2] += obj.trd["mov"][5]
    return obj


# runtime
if __name__ == "__main__":
    print("move thread bolck v10.0")
