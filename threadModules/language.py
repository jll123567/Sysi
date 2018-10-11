# lang handling
# module type: def
# feed=[in,out]
# in=[[vol,vol,vol],[Right version of sound]] each index is one mS
# out=[vol,vol,vol](mono output)


#
class audioSterio:
    def __init__(self, l=None, r=None):
        if l is None:
            self.l = []
        else:
            self.left = l
        if r is None:
            self.r = []
        else:
            self.right = r


class audioMono:
    def __init__(self, s=None):
        if s is None:
            self.s = []
        else:
            self.sound = s


class lang:
    def __init__(self, heard=audioSterio(), speakQue=audioMono()):
        self.heard = heard
        self.speakQue = speakQue

    # gets sound from input
    # Use: <obj> = Sysh.threadModules.language.listen(<obj>, <inputSource>)
    # Requires: obj, Audio Input
    def listen(self, inputSource):
        listining = 0
        while listining < 1000:
            self.heard.left.append(inputSource.l)
            self.heard.right.append(inputSource.r)
            listining += 1

    # tunes based on direction and minimum volume as an int
    # Use: <obj> = Sysh.threadModules.language.tune(<obj>, <int>, <int between -100 and 100> <same as last one>)
    # Requires: obj
    def tune(self, minVolume, minPan, maxPan):
        for i in self.heard.left:
            if abs(i) < minVolume:
                self.heard.left[self.heard.left.index(i)] = 0
            elif minPan > 0:
                self.heard.left[self.heard.left.index(i)] = 0
            elif abs(i) > minPan * (-2.2):
                self.heard.left[self.heard.left.index(i)] = 0
            else:
                continue

        for i in self.heard.right:
            if abs(i) < minVolume:
                self.heard.right[self.heard.left.index(i)] = 0
            elif maxPan < 0:
                self.heard.left[self.heard.left.index(i)] = 0
            elif abs(i) < maxPan * 2.2:
                self.heard.left[self.heard.left.index(i)] = 0
            else:
                continue

    # removes spoken audio
    # Use: <obj> = Sysh.threadModules.language.scilence(<obj>)
    # Requires: obj
    def silence(self):
        self.speakQue = []

    # sounds mono[vol0,vol1,vol2]

    # queue <sounds> to obj out
    # Use: <obj> = Sysh.threadModules.language.queueSpeak(<obj>, <sounds>)
    # Requires: obj, Mono Audio Input
    def queueSpeak(self, sounds):
        self.speakQue = sounds

    # output to an output obj
    # Use: <obj> = Sysh.threadModules.language.speak(<obj>, <place for output>)
    # Requires: obj with audio output
    def speak(self, outObj):
        out = outObj
        out.tag.update({"audioData": []})
        for i in self.speakQue.s:
            out.tag["audioData"].append(i)
        return out


# runtime
if __name__ == "__main__":
    print("language management v11.0")
