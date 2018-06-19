# import
import object

# setup
# lang
# feed=[in,out]
# in=[[vol,vol,vol],[Right version of sound]] each index is one mS
# out=[vol,vol,vol](mono output)


# gets sound from input
# Use: <obj> = Sysh.thread.language.listen(<obj>, <inputSource>)
# Requires: obj, Audio Input
def listen(obj, inputSource):
    listining = 0
    while listining < 1000:
        obj.trd["lang"][0].append(inputSource)
        listining += 1
    return obj


# sores audio data to ram
# Use: <obj> = Sysh.thread.language.store(<obj>)
# Requires: obj
def store(obj):
    dta = object.data(obj.trd["lang"][0], {})
    obj.trd["ram"].append(dta)
    return obj


# tunes based on direction and minimum volume as an int
# Use: <obj> = Sysh.thread.language.tune(<obj>, <int>, <int between -100 and 100> <same as last one>)
# Requires: obj
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


# removes spoken audio
# Use: <obj> = Sysh.thread.language.scilence(<obj>)
# Requires: obj
def silence(obj):
    obj.trd["lang"][1] = []
    return obj


# sounds mono[vol0,vol1,vol2]

# queue <sounds> to obj out
# Use: <obj> = Sysh.thread.language.queueSpeak(<obj>, <sounds>)
# Requires: obj, Mono Audio Input
def queueSpeak(obj, sounds):
    obj.trd["lang"][1] = sounds
    return obj


# output to an output obj
# Use: <obj> = Sysh.thread.language.speak(<obj>, <place for output>)
# Requires: obj with audio output
def speak(obj, outObj):
    for i in obj.trd["lang"][1]:
        outObj.tag["audioData"].append(i)
    return outObj


# runtime
if __name__ == "__main__":
    print("language management v11.0")
