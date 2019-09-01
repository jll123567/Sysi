"""don't mind me, just being dumb"""
import sys_objects
import re
a = sys_objects.sysObject()
b = a.dynamicFunction("def b():\n    print(\"a\")\n    print(\"c\")\n\n")
a.dynamicAttachFu(b, "b")
a.b()
