# import
import object

# setup
# lang
# feed=[in,out]
# in=[[vol,vol,vol],[Right version of sound]] each index is one mS
# out=[vol,vol,vol](mono output)

listing = False
out = []


def listen(obj, inputSource):
    global listing
    listing = True
    while listing:
        obj.trd["lang"][0].append(inputSource)
    return obj


def store(obj):
    dta = object.data(obj.trd["lang"][0], {})
    obj.trd["ram"].append(dta)
    return obj


def tune(obj, minVolume, minPan, maxPan):
    for i in obj.trd["lang"][0][0]:
        if abs(i) < minVolume:
            obj.trd["lang"][0][0][obj.trd["lang"][0][0].index(i)] = 0
        elif minPan > 0:
            obj.trd["lang"][0][0][obj.trd["lang"][0][0].index(i)] = 0
        elif abs(i) > minPan * (-2.2):
            obj.trd["lang"][0][0][obj.trd["lang"][0][0].index(i)] = 0
        else:
            continue

    for i in obj.trd["lang"][0][1]:
        if abs(i) < minVolume:
            obj.trd["lang"][0][1][obj.trd["lang"][0][0].index(i)] = 0
        elif maxPan < 0:
            obj.trd["lang"][0][0][obj.trd["lang"][0][0].index(i)] = 0
        elif abs(i) < maxPan * 2.2:
            obj.trd["lang"][0][0][obj.trd["lang"][0][0].index(i)] = 0
        else:
            continue
    return obj


def silence(obj):
    obj.trd["lang"][1] = []
    return obj


# sounds mono[vol0,vol1,vol2]

def queueSpeak(obj, sounds):
    obj.trd["lang"][1] = sounds
    return obj


def speak(obj):
    global out
    for i in obj.trd["lang"][1]:
        out.append(i)
    obj.trd["lang"][1] = []
    return obj


# runtime
if __name__ == "__main__":
    print("language management v10.0")
