# A definition for a privacy method and a text obfuscator
# module type: standard
# obj.tag
#    {"priv":[]}
#        [[<obj> is public to(knows me)],[objects public to <obj>(i know)]]

import re


# make o1 private to o0
# o0(obj)*, o1(obj)
# No output
def MakePrivate(o0, o1):
    for i in o0.tag["priv"][1]:
        if i == o1:
            o0.tag["priv"][1].pop(o0.tag["priv"][1].index(o1))


# make o0 and o1 public to each other
# o0(obj)*, o1(obj)*
# No output
def makePublic(o0, o1):
    o0.tag["priv"][0].append(o1)
    o0.tag["priv"][1].append(o1)
    o1.tag["priv"][0].append(o0)
    o1.tag["priv"][1].append(o0)


# make o1 public to o0 without o1's knowledge
# o0(obj)*, o1(obj)*
# No output
def intrude(o0, o1):
    o0.tag["priv"][1].append(o1)


def obscureText(text, method):
    if method == 0:
        return text
    elif method == 1:
        soonToArrive = False
        output = ""
        output += text[1]
        for i in text:
            if soonToArrive:
                if re.match(r"\w+", i):
                    output += i
                    soonToArrive = False
            if i == " ":
                soonToArrive = True
    elif method == 2:
        spaces = 0
        for i in text:
            if i == ' ':
                spaces += 1
        spaces += 1
        print("." * spaces)
    elif method == 3:
        return ""
    else:
        print("not a valid method")


# runtime
if __name__ == "__main__":
    print(" privacy v11.0")
