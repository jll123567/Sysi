"""Handle sounds.

audioStereo: stereo audio hold
audioMono: mono audio hold
lang: audio threadModule
"""
import sys_objects


# left input([int]), right input([int])
class audioStereo:
    """Hold stereo audio."""

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
    """Hold mono audio."""

    def __init__(self, sound=None):
        if sound is None:
            self.sound = []
        else:
            self.sound = sound


# heard audio(audioStereo), spoken(audioMono)
class lang:
    """Hold and manipulate audio."""

    def __init__(self, heard=audioStereo(), speakQue=audioMono()):
        self.heard = heard
        self.speakQue = speakQue

    # gets sound from input
    # inputSource(audioStereo)*
    # none
    def listen(self, inputSource):
        """Get sound from input and append it to heard."""
        self.heard.left.append(inputSource.l)
        self.heard.right.append(inputSource.r)

    def tune(self, minVolume, minPan, maxPan):
        """Check if audio is above a minimum volume or within a pan range and if its not cut it.

        Min volume is in Db
        pan is a float range from -1.0 to 1.0
        minPan is the smallest pan value
        maxPan is the largest pan value
        """

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
        """Clear spoken audio."""
        self.speakQue = []

    def queueSpeak(self, sounds):
        """Add sounds to the speaking queue"""
        self.speakQue = sounds

    def package(self):
        """Pack audio data into a data obj and return it."""
        return sys_objects.data([self.heard, self.speakQue], {"name": "tread.lang.package", "id": None,
                                                                 "dataType": "thread.lang.package"})
