"""don't mind me, just being dumb"""
import sys_objects

a = sys_objects.sysObject()
a.a = "hhh"
f = "def g(self):\n    def gg(o):\n        f = \"\"\n        for i in range(3):\n            f +=o.a+\'s\'\n        return f\n    ff=gg(self)\n    print(ff)\n"
b = a.dynamicFu(f)
a.dynamicAttachFu(b, "b")
a.dynamicBindFu("b")
a.b()
