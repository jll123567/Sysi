import object
import prog.save as objSave
f = object.user()
print(f.tag)

def wth(defaultArg=[]):
    print("I have ", defaultArg, "to say")
objSave.saveObj(f, "g.obj")