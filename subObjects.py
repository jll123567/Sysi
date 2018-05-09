# setup

# objects can be like groups without being groups
# parent and child objects have a "sub" section in their thread

# "sub": {"parent": <parent obj refernce>, "children": [[refrence, "position"], ...]}

# refrences can be to any obj
# position is the distance from the curent object's model origin in the fromat "x,y,z"
# if a object has no children but a prent leave "children" set to an empty list ([])
# if a object has no parent set "parent" to None
# if an object has neither chilldren or a parent remove the "sub" entry or set it to None
# children's model position are overidien in the parent.trd["sub"]

# ex parent: "sub": {"parent": None, "children": [[child0, "10,10,20.553"]]}
# ex child: "sub": {"parent": parent0, "children":[[child1, "1,1,1"]]}

def makeEmptyParrent(obj):
    obj.trd.update({"sub": {"parent": None, "children": []}})
    return obj


def makeParent(obj, children):
    obj.trd.update({"sub": {"parent": None, "children": children}})
    return obj


def makeChild():



def setParent():



def setChildren():



def removeParent():



def removeSub():



