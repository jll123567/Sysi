import tkinter as tk


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.fLeft = tk.Frame(self)
        self.fLeft.pack(side="left", padx=5, pady=5)

        self.fRight = tk.Frame(self)
        self.fRight.pack(side="right", padx=5, pady=5)

        self.hi_there = tk.Button(self.fRight)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        # self.hi_there["geometry"] = "75x75"
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self.fRight, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

        self.yo = tk.Button(self.fLeft, text="Yo dawg!", fg="blue", command=self.youFuckedUp)
        self.yo.pack()

    def say_hi(self):
        print("hi there, everyone!")

    def youFuckedUp(self):
        def sayFuck():
            print("you really fucked up now...")

        self.hi_there["text"] = "you fucked up"
        self.hi_there["fg"] = "red"
        self.hi_there["command"] = sayFuck


class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()

        self.entrythingy = tk.Entry()
        self.entrythingy.pack()

        # here is the application variable
        self.contents = tk.StringVar()
        # set it to some value
        self.contents.set("this is a variable")
        # tell the entry widget to watch this variable
        self.entrythingy["textvariable"] = self.contents

        # and here we get a callback when the user hits return.
        # we will have the program print out the value of the
        # application variable when the user hits return
        self.entrythingy.bind('<Key-Return>',
                              self.print_contents)

    def print_contents(self, event):
        print("hi. contents of entry is now ---->",
              self.contents.get(), "\n", str(event))


root = tk.Tk()
app = Application(master=root)
app.master.title("funky name")
app.mainloop()
exit(0)
