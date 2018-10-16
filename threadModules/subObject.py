# Sub object grouping type
# module type: def

# objects can be like groups without being groups
# parent and child objects have a "sub" section in their threadModules

# "sub": {"parent": [reference, offset], "children": [reference, ...]}

# reference:objId
# offset: is the distance of the  parent's position to the object's position in the format [x,y,z]
# if an object has one child put it in a list by its self
# if a object has no children but a prent leave "children" set to an empty list ([])
# if a object has no parent set "parent" to None
# if an object has neither children or a parent remove the "sub" entry or set it to None
# children's move becomes child.mov = "sub"

# ex parent: "sub": {"parent": None, "children": [child0]}
# ex child: "sub": {"parent": [parent0, [1,1,1]], "children":[child1]}


# Sub object
# parent([objId(str), [x,y,z]]/None), children([obj]/[])
class sub:
    def __init__(self, parent=None, children=None):
        self.parent = parent
        if children is None:
            self.children = []
        else:
            self.children = children

    # sets parent
    # parent(obId(str)), offset([x,y,z])
    # none
    def setParent(self, parent, offset):
        self.parent = [parent, offset]

    # set children
    # children([child(objId(str))])
    # none
    def setChildren(self, children):
        self.children = children

    # add a child to a parent
    # child(objId(str))
    # none
    def addChild(self, child):
        self.children.append(child)

    # remove child rom parent
    # index(int)
    # none
    def removeChild(self, index):
        self.children.pop(index)


# Info at run
if __name__ == "__main__":
    print("Sub object grouping type\nmodule type: def")
