order = []


class display:
    def __init__(self, size, rotation, distance, in_use):
        self.size = size
        self.rotation = rotation
        self.distance = distance
        self.in_use = in_use

    def set(self, size, rotation, distance):
        self.size = size
        self.rotation = rotation
        self.distance = distance

    def add(self, size, rotation, distance):
        self.size = size
        self.rotation = rotation
        self.distance = distance
        self.in_use = True

    def remove(self):
        self.size = [0, 0]
        self.rotation = 0
        self.distance = 0
        self.in_use = False


class window:
    def __init__(self, size, in_use, name, display, location):
        self.size = size
        self.display = display
        self.in_use = in_use
        self.name = name
        self.location = location

    def open(self, size, name, display, ):
        global order
        self.size[0] = size
        self.name = name
        self.in_use = True
        self.display = display
        self.location[0] = [((self.display.size[0] / 2) - self.size[0][0]),
                            ((self.display.size[1] / 2) - self.size[0][1])]
        order.insert(0, self.name)

    def close(self):
        global order
        order.remove(self.name)
        self.size = [0, 0]
        self.name = None
        self.in_use = False
        self.display = None
        self.location[0] = [0, 0]

    def min(self):
        self.blur()
        self.size[1] = self.size[0]
        self.size[0] = [0, 0]
        self.location[1] = self.location[0]
        self.location[0] = [-1, -1]

    def norm(self):
        self.focus()
        self.size[0] = self.size[1]
        self.location[0] = self.location[1]

    def max(self):
        self.focus()
        self.size[1] = self.size[0]
        self.size[0] = self.display.size
        self.location[1] = self.location[0]
        self.location[0] = [0, 0]

    def move(self, location):
        self.location[1] = self.location[0]
        self.location[0] = location

    def resize(self, size):
        self.size[1] = self.size[0]
        self.size[0] = size

    def focus(self):
        global order
        order.remove(self.name)
        order.insert(0, self.name)

    def blur(self):
        global order
        i = order.index(self.name)
        order.remove(self.name)
        order.insert(i + 1, self.name)


        # runtime


if __name__ == "__main__":
    print("display definitions")
    # display_0=display(None,None,None,None)
    # display_0.remove()
    # display_0.add([333,333],0,500)


# by jacob ledbetter