# import
import time


# setup
# tasker
# tsk=[profile,profile,profile,...]
# profile=[f0,f1,f2,...]

class tsk:
    def __init__(self, current=[], profiles=[]):
        self.current = current
        self.profiles = profiles

    def nextCurrent(self):
        if self.profiles != []:
            if isinstance(self.profiles[0], list):
                self.current = self.profiles[0]
            else:
                self.current = [self.profiles[0]]
            self.profiles.pop(0)
        else:
            self.current = []

    # steps through each command in current profile
    # use <self> = Sysh.thread.tasker.step(<self>)
    # requires: self
    def step(self):
        print(self.current[0])
        self.current.pop(0)
        if self.current == []:
            if self.profiles == []:
                print("No remaining operations")
            else:
                self.nextCurrent()

    # runs entire profile
    # use <self> = Sysh.thread.tasker.run(<self>)
    # requires: self
    def run(self):
        for i in self.current:
            print(i)
        self.nextCurrent()

    # sets the current profile to <profile>
    # use <self> = Sysh.thread.tasker.setCurrentProfile(<self>, <task profile>)
    # requires: self
    def setCurrentProfile(self, profile):
        self.current = profile

    # adds a new profile to the end of the tasking queue
    # use <self> = Sysh.thread.tasker.addProflie(<self>, <task profile>)
    # requires: self
    def addProfile(self, profile):
        self.profiles.append(profile)

    # ends a task
    # use <self> = Sysh.thread.tasker.quitTask(<self>, <index>)
    # requires: self
    def quitTask(self, index):
        self.profiles.pop(index)

    # waits <t> seconds before running <self>
    # use <self> = Sysh.thread.tasker.wait(<self>, <int/float>)
    # requires: self
    def wait(self, t):
        time.sleep(t)
        self.run()

    # set the following task to loop infinately
    # use self.loop(profile)
    # requires self
    def loop(self, profile):
        name = ""
        for char in profile[0]:
            if char == '.':
                break
            else:
                name += char
        name += ".trd.tsk"
        self.addProfile([profile, [name, "loop", [profile]]])

# runtime
if __name__ == "__main__":
    print("tasker v11.0")
