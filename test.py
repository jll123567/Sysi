import object as Sobject
import thread.move as move

obj = Sobject.object()
obj.trd.mov = move.mov()
obj.trd.mov.warp(1, 1, 1)
obj.tag.update({"name": "testObj"})
print(obj.__dict__)
print(obj.trd.__dict__)
print(obj.trd.mov.__dict__)