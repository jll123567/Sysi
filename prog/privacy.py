#obj.tag
#    {"priv":[]}
#        [[obj is public to(they know)],[objects public to obj(i know)]]

def MakePrivate(o0,o1):
    for i in o0.tag["priv"][1]:
        if i==o1:
            o0.tag["priv"][1].pop(o0.tag["priv"][1].index(o1))
            
def makePublic(o0,o1):
    o0.tag["priv"][0].append(o1)
    o0.tag["priv"][1].append(o1)
    o1.tag["priv"][0].append(o0)
    o1.tag["priv"][1].append(o0)

def intrude(o0,o1):
    o0.tag["priv"][1].append(o1)
    
if __name__ == "__main__":
    print(" privacy v10.0")

# by Jacob Ledbettervf