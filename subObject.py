# setup

# objects can be like groups without being groups
# parent and child objects have a "sub" section in their thread

# "sub": {"parent": [reference, offset], "children": [reference, ...]}

# references can be to any obj
# offset is the distance of the  parent's position to the object's position in the format [x,y,z]
# if an object has one child put it in a list by its self
# if a object has no children but a prent leave "children" set to an empty list ([])
# if a object has no parent set "parent" to None
# if an object has neither children or a parent remove the "sub" entry or set it to None
# children's model position are overridden in the parent.trd["sub"]

# ex parent: "sub": {"parent": None, "children": [child0]}
# ex child: "sub": {"parent": [parent0, [1,1,1]], "children":[child1]}


def makeEmptyParent(obj):
    obj.trd.update({"sub": {"parent": None, "children": []}})
    return obj


def makeParent(obj, children):
    obj.trd.update({"sub": {"parent": None, "children": children}})
    return obj


def makeChild(obj, parent, offset):
    obj.trd.update({"sub": {"parent": [parent, offset], "children": []}})
    obj.trd["mov"] = "sub"
    return obj


def setParent(obj, parent, offset):
    obj.trd["sub"]["parent"] = [parent, offset]
    obj.trd["mov"] = "sub"
    return obj


def setChildren(obj, children):
    obj.trd["sub"]["children"] = children
    return obj


def addChild(obj, child):
    obj.trd["sub"]["children"].append(child)
    return obj


def removeChild(obj, index):
    obj.trd["sub"]["children"].pop(index)
    return obj


def removeParent(obj):

    def getParentMov(obj):
        par = obj.trd["sub"]["parent"][0]
        if par.trd["mov"] == "sub":
            return getParentMov(par)
        else:
            return par.trd["mov"]

    parentMov = getParentMov(obj)
    offset = obj.trd["sub"]["parent"][1]
    obj.trd["mov"] = [parentMov[0] + offset[0], parentMov[1] + offset[1], parentMov[2] + offset[2],
                      parentMov[3], parentMov[4], parentMov[5]]
    obj.trd["sub"]["parent"] = None
    return obj


def removeSub(obj):
    del obj.trd["sub"]
    return obj


# runtime
if __name__ == "__main__":
    print("subObjects v10")
# to test
# functions
# assemblies and non assemblies
# many children
# mov updating
