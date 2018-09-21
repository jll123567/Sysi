# import


# setup
# server=dta
# [[usrlist],     [channels]]
# usrlist = [atribs,is_admin]
# channels = [name,msg,stream,perms]
# perm = ["name:text"][level,[users,...]][r,w,s,l]


# ##I WILL UPDATE THIS AT A LATER DATE## #

def addServer(server, pram):
    server.storage = pram


def delServer(server, usr):
    for i in server.storage[0]:
        if i[0] == usr:
            if i[1]:
                print(server.tag["name"], " removed")
                server.storage = None
                server.tag = None
            else:
                print("access denied:must be admin")


def addChannel(server, chName, perms, usr):
    for i in server.storage[0]:
        if i[0] == usr.tag["id"]:
            if i[1]:
                server.storage[1].append(["#" + chName, ["channel #" + chName + " was created"], [0, 0], perms])
            else:
                print("access denied:must be admin")


def delChannel(server, channel, usr):
    for i in server.storage[0]:
        if i[0] == usr.tag["id"]:
            if i[1]:
                count = 0
                for f in server.storage[1]:
                    if channel == f[0]:
                        server.storage[1].pop(count)
                        print(channel, " removed")
                    else:
                        count += 1


def addMessage(server, channel, message, usr):
    count = 0
    for i in server.storage[0]:
        if i[0] == usr.tag["id"]:
            for f in server.storage[1]:
                if f[0] == channel:
                    if f[3][count]:
                        f[1].append(usr.tag["name"] + ":" + message)
                    else:
                        print("can not add message: atribs not permitted")
        else:
            count += 1


def delMessage(server, channel, index, usr):
    for i in server.storage[0]:
        if i[0] == usr.tag["id"]:
            if i[1]:
                for f in server.storage[1]:
                    if f[0] == channel:
                        f[1].pop(index)
            else:
                for f in server.storage[1]:
                    if f[0] == channel:
                        if usr.tag["id"] == f[1][index][0, len(usr.tag["id"])]:
                            f[1].pop(index)


def invite(server, usr, is_admin):
    server.storage[0].append([usr.tag["id"], is_admin])


def removeUser(server, usr):
    count = 0
    for i in server.storage[0]:
        if i[0] == usr.tag["id"]:
            server.storage[0].pop(count)
        else:
            count += 1


def joinStream(server, channel, usr):
    for i in server.storage[1]:
        if i[1] == channel:
            i[2][2].append([usr.tag["id"], usr.trd["lang"][1]])


def updateStream(server, channel):
    for i in server.storage[1]:
        if i[0] == channel:
            i[2][0] = 0
            for f in i[2][1]:
                count = 0
                for g in server.storage[0]:
                    if g == f[1]:
                        if i[3][count][2]:
                            i[2][0] += f[1]
                    else:
                        count += 1
            if i[2][0] > 100:
                i[2][0] = 100


def streamListen(server, channel, usr):
    for i in server.storage[1]:
        if i[0] == channel:
            count = 0
            for f in server.storage[0]:
                if usr.tag["id"] == f[0]:
                    if i[3][count][3]:
                        connectedToStream = True
                        while connectedToStream:
                            usr.thread.language.listen(i[2][0])
                            n = input("dc?")
                            if n == 'y':
                                connectedToStream = False
                            else:
                                continue
                    else:
                        count += 1


def msgDisplay(server, channel, usr):
    for i in server.storage[1]:
        if i[0] == channel:
            count = 0
            for f in server.storage[0]:
                if usr.tag["id"] == f[0]:
                    if i[3][count][3]:
                        for g in i[1]:
                            print(g)
                    else:
                        count += 1


# runtime
if __name__ == "__main__":
    print("system chat v11.0")
