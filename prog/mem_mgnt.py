import re
import thread.random_access_memory


# mem[internal,real,storage]
# [obj,obj,...]stored in order of date added
def load(usr, dir, index):
    if dir == 0:
        print("no internal access")
    else:
        thread.random_access_memory.load(usr.trd["ram"], usr.mem[dir][index])


def forget(user, dir, index):
    if dir == 0:
        print("no internal access")
    else:
        user.mem[dir].pop(index)


def store(user, dir, object):
    if dir == 0:
        print("no internal access")
    else:
        user.mem[dir].append(object)


def find(user, query):
    if query == None:
        query = input()
    for d in range(1, 2):
        for i in user.mem[d]:
            for t in i.tag:
                if re.match(str(t), r"*(.)" + query + r"*(.)"):
                    print(t)
                else:
                    print(None)


def modify(user, dir, index, value):
    if dir == 0:
        print("no internal access")
    else:
        user.mem[dir][index] = value


if __name__ == "__main__":
    print("user memory v10.0")


# by jacob ledbetter