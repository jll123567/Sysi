# Model format=[[scale,"x,y,z-x,y,z","..."],[scale,["x,y,z",["x,y,z","..."],["x,y,z","..."]],[that,all,again]],
# [scale,[[["original skpos","new pos","next"],[data for next point]],[next animation]]],material] assem [[scale,["x,
# y,z,p,ya,r",obj] and material = "assem"


def make_model(model, obj, material):
    obj.mod[0] = model
    obj.mod[3] = material
    """else:
        points=[[]]
        working=True
        while working:
            if points=[[]]:
                points.insert(0,input("scale from a(1mm=100000000a so 100000000)"))
            x1=0
            y1=0
            z1=0
            print("first point of new edge from origin")
            x1=input("x:")
            y1=input("y:")
            z1=input("z:")
            x2=0
            y2=0
            z2=0
            print("second point of new edge from origin")
            x2=input("x:")
            y2=input("y:")
            z2=input("z:")
            points[1].append(str(str(x1)+","+str(y1)+","+str(z1)+"-"str(x2)+","str(y2)+","str(z2))
            check=input("are you done(y/n)")
            if check="y":
                working=False
        object.mod[0]=points"""


def rig_model(rigging, obj):
    obj.mod[1] = rigging


def set_animations(obj, ani):
    obj.mod[2] = ani


def add_animation(animation, obj):
    obj.mod[2].append(animation)


def display_model(obj):
    for f in obj.mod[0]:
        if type(f) == type([]):
            display_model(f[1])
            print("@" + f[0])
        elif type(f) == type(""):
            print("scale:" + f + "a for each unit")
        else:
            print(f)
    for i in obj.mod[1]:
        print(i[0])
        for f in i[1, 2]:
            print(f)
    print(obj.mod[2][0], "frames per second")
    for i in obj.mod[2][1]:
        print(i)
    print("material:", obj.mod[3])


def new_assem(obj, assm, ani, rig):
    obj.mod[0] = assm
    obj.mod[1] = rig
    obj.mod[2] = ani
    obj.mod[3] = "assem"


if __name__ == "__main__":
    print("model rigging and viewer v10.0")

# by jacob ledbetter"""
