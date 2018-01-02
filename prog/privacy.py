# import
import re


# setup
# obj.tag
#    {"priv":[]}
#        [[<obj> is public to(they know)],[objects public to <obj>(i know)]]
def MakePrivate(o0, o1):
    for i in o0.tag["priv"][1]:
        if i == o1:
            o0.tag["priv"][1].pop(o0.tag["priv"][1].index(o1))


def makePublic(o0, o1):
    o0.tag["priv"][0].append(o1)
    o0.tag["priv"][1].append(o1)
    o1.tag["priv"][0].append(o0)
    o1.tag["priv"][1].append(o0)


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
        print("."*spaces)
    elif method == 3:
        return ""
    else:
        print("not a valid method")


# runtime
if __name__ == "__main__":
    print(" privacy v10.0")
