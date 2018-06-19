# import
from . import move


# setup
def attract(o0, o1, force):
    if o0.trd["mov"][0] > o1.trd["mov"][0]:
        o0.trd["mov"][3] = (force * -1)
    elif o0.trd["mov"][0] < o1.trd["mov"][0]:
        o0.trd["mov"][3] = force
    else:
        o0.trd["mov"][3] = 0
    if o0.trd["mov"][1] > o1.trd["mov"][1]:
        o0.trd["mov"][4] = (force * -1)
    elif o0.trd["mov"][1] < o1.trd["mov"][1]:
        o0.trd["mov"][4] = force
    else:
        o0.trd["mov"][4] = 0
    if o0.trd["mov"][2] > o1.trd["mov"][2]:
        o0.trd["mov"][5] = (force * -1)
    elif o0.trd["mov"][2] < o1.trd["mov"][2]:
        o0.trd["mov"][5] = force
    else:
        o0.trd["mov"][5] = 0
    o0 = move.move(o0)
    return o0


def repel(o0, o1, force):
    if o0.trd["mov"][0] > o1.trd["mov"][0]:
        o0.trd["mov"][3] = force
    elif o0.trd["mov"][0] < o1.trd["mov"][0]:
        o0.trd["mov"][3] = force * -1
    else:
        o0.trd["mov"][3] = 0
    if o0.trd["mov"][1] > o1.trd["mov"][1]:
        o0.trd["mov"][4] = force
    elif o0.trd["mov"][1] < o1.trd["mov"][1]:
        o0.trd["mov"][4] = force * -1
    else:
        o0.trd["mov"][4] = 0
    if o0.trd["mov"][2] > o1.trd["mov"][2]:
        o0.trd["mov"][5] = force
    elif o0.trd["mov"][2] < o1.trd["mov"][2]:
        o0.trd["mov"][5] = force * -1
    else:
        o0.trd["mov"][5] = 0
    o0 = move.move(o0)
    return o0


# runtime
if __name__ == "__main__":
    print("physx v11.0")
