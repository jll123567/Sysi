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


# noinspection PyDefaultArgument
class sub:
    def __init__(self, parent=None, children=[]):
        self.parent = parent
        self.children = children

    def setChildren(self, children):
        self.children = children

    def addChild(self, child):
        self.children.append(child)

    def removeChild(self, index):
        self.children.pop(index)


# runtime
if __name__ == "__main__":
    print("subObjects v10")
