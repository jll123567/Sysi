"""lang handling"""
import object


# left input([int]), right input([int])
class audioStereo:
    """stereo audio"""
    def __init__(self, left=None, right=None):
        if left is None:
            self.left = []
        else:
            self.left = left
        if right is None:
            self.right = []
        else:
            self.right = right


# sound input([int])
class audioMono:
    """mono audio"""
    def __init__(self, sound=None):
        if sound is None:
            self.sound = []
        else:
            self.sound = sound


# heard audio(audioStereo), spoken(audioMono)
class lang:
    """language thread module class"""
    def __init__(self, heard=audioStereo(), speakQue=audioMono()):
        self.heard = heard
        self.speakQue = speakQue

    # gets sound from input
    # inputSource(audioStereo)*
    # none
    def listen(self, inputSource):
        """gets sound from input and appends it to heard"""
        self.heard.left.append(inputSource.l)
        self.heard.right.append(inputSource.r)

    def tune(self, minVolume, minPan, maxPan):
        """check if audio is above a minimum volume or withing a pan range and if its not cut it
        min volume is in Db
        pan is a float range
        minPan is the smallest pan value(up to -1.0)
        maxPan is the largest pan value(up to 1.0)"""
        for i in self.heard.left:
            if abs(i) < minVolume:
                self.heard.left[self.heard.left.index(i)] = 0
            elif minPan > 0:
                self.heard.left[self.heard.left.index(i)] = 0
            elif abs(i) > minPan * -100:
                self.heard.left[self.heard.left.index(i)] = 0
            else:
                continue

        for i in self.heard.right:
            if abs(i) < minVolume:
                self.heard.right[self.heard.right.index(i)] = 0
            elif maxPan < 0:
                self.heard.right[self.heard.right.index(i)] = 0
            elif abs(i) < maxPan * 100:
                self.heard.right[self.heard.right.index(i)] = 0
            else:
                continue

    def silence(self):
        """clear spoken audio"""
        self.speakQue = []

    def queueSpeak(self, sounds):
        """add sounds to the speaking queue"""
        self.speakQue = sounds

    def package(self):
        """pack audio data into a data obj to send to ram and return it"""
        return object.data([self.heard, self.speakQue], {"name": "tread.lang.package", "id": None,
                                                                 "dataType": "thread.lang.package"})
