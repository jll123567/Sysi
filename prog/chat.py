# import
import thread.language


# code
# def
# server=dta
# [[usrlist],     [channels]]
# [user,is_admin] [name,msg,stream,perms]
#                      ["name:text"][level,[users,...]][r,w,s,l]
def addServer(server, pram):
    server.d = pram


def delServer(server, uname):
    for i in server.d[0]:
        if i[0] == uname:
            if i[1]:
                print(server.tag["name"], " removed")
                server.d = None
                server.tag = None
            else:
                print("access denied:must be admin")


def addChannel(server, name, perms, usr):
    for i in server.d[0]:
        if i[0] == usr.tag["name"]:
            if i[1] == True:
                server.d[1].append(["#" + name, ["channel #" + name + " was created"], [0, 0], perms])
            else:
                print("access denied:must be admin")


def delChannel(server, channel, usr):
    for i in server.d[0]:
        if i[0] == usr.tag["name"]:
            if i[1] == True:
                count = 0
                for f in server.d[1]:
                    if channel == f[0]:
                        server.d[1].pop(count)
                        print(channel, " removed")
                    else:
                        count += 1


def addMessage(server, channel, message, usr):
    count = 0
    for i in server.d[0]:
        if i[0] == usr.tag["name"]:
            for f in server.d[1]:
                if f[0] == channel:
                    if f[3][count] == True:
                        f[1].append(usr.tag["name"] + ":" + message)
                    else:
                        print("can not add message: user not permitted")
        else:
            count += 1


def delMessage(server, channel, index, usr):
    for i in server.d[0]:
        if i[0] == usr.tag["name"]:
            if i[1] == True:
                for f in server.d[1]:
                    if f[0] == channel:
                        f[1].pop(index)
            else:
                for f in server.d[1]:
                    if f[0] == channel:
                        if usr.tag["name"] == f[1][index][0, len(usr.tag["name"])]:
                            f[1].pop(index)


def invite(server, usr, is_admin):
    server.d[0].append([usr.tag["name"], is_admin])


def removeUser(server, usr):
    count = 0
    for i in server.d[0]:
        if i[0] == usr.tag["name"]:
            server.d[0].pop(count)
        else:
            count += 1


def joinStream(server, channel, usr):
    for i in server.d[1]:
        if i[1] == channel:
            i[2][2].append([usr.tag["name"], usr.trd["lang"][1]])


def updateStream(server, channel):
    for i in server.d[1]:
        if i[0] == channel:
            i[2][0] = 0
            for f in i[2][1]:
                count = 0
                for g in server.d[0]:
                    if g == f[1]:
                        if i[3][count][2] == True:
                            i[2][0] += f[1]
                    else:
                        count += 1
            if i[2][0] > 100:
                i[2][0] = 100


def streamListen(server, channel, usr):
    for i in server.d[1]:
        if i[0] == channel:
            count = 0
            for f in server.d[0]:
                if usr.tag["name"] == f[0]:
                    if i[3][count][3] == True:
                        thread.language.listen(usr, i[2][0])
                    else:
                        count += 1


def msgDisplay(server, channel, usr):
    for i in server.d[1]:
        if i[0] == channel:
            count = 0
            for f in server.d[0]:
                if usr.tag["name"] == f[0]:
                    if i[3][count][3] == True:
                        for g in i[1]:
                            print(g)
                    else:
                        count += 1



                        # runtime


if __name__ == "__main__":
    print("system chat v10.0")
# notes

# auth
"""by jacob ledbetter"""
