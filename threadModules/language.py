# lang handling
# module type: def
# feed=[in,out]
# in=[[amplitude,amplitude,amplitude],[Right version of sound]] each index is one mS
# out=[amplitude,amplitude,amplitude](mono)
import object


# stereo audio for lang
# left input([int]), right input([int])
class audioStereo:
    def __init__(self, left=None, right=None):
        if left is None:
            self.left = []
        else:
            self.left = left
        if right is None:
            self.right = []
        else:
            self.right = right


# mono audio
# sound input([int])
class audioMono:
    def __init__(self, sound=None):
        if sound is None:
            self.sound = []
        else:
            self.sound = sound


# language thread module
# heard audio(audioStereo), spoken(audioMono)
class lang:
    def __init__(self, heard=audioStereo(), speakQue=audioMono()):
        self.heard = heard
        self.speakQue = speakQue

    # gets sound from input
    # inputSource(audioStereo)*
    # none
    def listen(self, inputSource):
        listening = 0
        while listening < 1000:
            self.heard.left.append(inputSource.l)
            self.heard.right.append(inputSource.r)
            listening += 1

    # tunes based on direction and minimum volume as an int
    # min Volume to reeve(int)*, minimum panning(int -100(l) to 100(r))*, maximum panning(int -100(l) to 100(r))*
    # todo make pan -1 to 1 float
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

    # clears spoken audio
    # none
    # none
    def silence(self):
        self.speakQue = []

    # queue <sounds> to obj out
    # sounds(audioMono)*
    # none
    def queueSpeak(self, sounds):
        self.speakQue = sounds

    # pack data for ram
    # none
    # dta(cpx attribs, tags)
    def package(self):
        return object.data([self.heard, self.speakQue], {"name": "tread.lang.package", "id": None,
                                                                 "dataType": "thread.lang.package"})


# info at run
if __name__ == "__main__":
    print("lang handling\nmodule type: def")
