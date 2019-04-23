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
text = "[\"im a stupid pram]\"]"
text2 = ""

for i in text:
    if i == ']':
        break
    text2 += i
print(text2)

text = "OPERATION{\"a\",\"b\",[\"im a stupid pram]\"],\"d\"}"
text2 = re.search(r"\[(.*)\]", text).group(1)
print(text2)
