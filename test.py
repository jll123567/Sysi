"""don't mind me, just being dumb"""
# TODO: make a "programming language" for tsk operations. Something simple.
# import prog.threadCompiler as threadComp
# import thread_modules.tasker
# a = threadComp.parseFile("f.txt")
# print(a)
# if isinstance(a, thread_modules.tasker.tsk):
#     print("profile:\n\t", a.profile)
#     print("current:\n\t", a.current)
import re
import prog.threadCompiler as threadComp

text = "SHIFT{}"
print(threadComp.formatShift(text))


