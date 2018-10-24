import object
import prog.save as objSave
f = object.user()

def printTag(self):
    print(self.tag)

setattr(f, "printTag", MethodTest)