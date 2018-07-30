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
        if isInsance(self.profiles[0], list):
            self.current = self.profiles[0]
        else:
            self.current.append(self.profiles[0])
        self.profiles.pop(0)

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


# runtime
if __name__ == "__main__":
    print("tasker v10.0")
