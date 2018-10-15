# Sub object grouping type
# module type: def

# objects can be like groups without being groups
# parent and child objects have a "sub" section in their threadModules

# "sub": {"parent": [reference, offset], "children": [reference, ...]}

# references can be to any obj
# offset is the distance of the  parent's position to the object's position in the format [x,y,z]
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

# sets parent to todo finish this
    def setParent(self, parent, offset):
        self.parent = [parent, offset]

    def setChildren(self, children):
        self.children = children

    def addChild(self, child):
        self.children.append(child)

    def removeChild(self, index):
        self.children.pop(index)


# runtime
if __name__ == "__main__":
    print("subObjects v11")
