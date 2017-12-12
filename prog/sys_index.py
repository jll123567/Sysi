from time import sleep
import object


# format: dta([head,body,id],tags)
index=[]
last_id = 0


def newPage(head, body, tags):
    global index, last_id
    index.d.append(object.data([head, body, last_id + 1], tags))
    last_id += 1


def readPage(id):
    global index
    for i in index.d:
        if i.d[2] == id:
            print("    ", i.d[0])
            print("\n", i.d[1])
            print("\nend of entry\n\n", id)


def quickRead(id):
    global index
    for i in index.d:
        if i.d[2] == id:
            for f in i.d[0]:
                print(f)
            sleep(1)
            for f in i.d[1]:
                print(f)
            sleep(1)
            print(i.d[2])


def updatePage(head, body, idToModify):
    global index
    for i in index.d:
        if i.d[2] == idToModify:
            if head != None:
                i.d[0] = head
            if body != None:
                i.d[1] = body


def deletePage(id):
    global index
    for i in index.d:
        if i.d[2] == id:
            index.d.pop(index(i))


if __name__ == "__main__":
    print("system index v10.0")


# by jacob ledbetter
