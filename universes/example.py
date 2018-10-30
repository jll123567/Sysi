# imports
import object
import prog.idGen

# user defined functions
# def ab():
#   print("ab" *10)

# objects
a = object.object()
a.mod = 'a'
# setattr(a, "ab", ab)
a.tag["name"] = "a"

# containers
masterCont = object.container()
masterCont.bnd = [None]
masterCont.tag["name"] = "example/masterCont"

# scenes
scene0 = object.scene()
scene0.cont = masterCont
scene0.obj.append(a)
scene0.tag["name"] = "the beginning"

# uni
example = object.universe()
example.obj.append(a)
example.scn.append(scene0)
example.cont.append(masterCont)
