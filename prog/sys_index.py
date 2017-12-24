# import
from time import sleep
import object

# setup
# format:
# dta([head,body,id],tags)
last_id = 0
index = object.data([object.data(["Hello, world!", "sysh V10.0 is here. Hope you're hyped. :D", 1],
                                 {'uni': 'main', 'id': 'idx1', 'name': 'Hello, world!',
                                  'terms': ['sys', 'Hello,world!', 'v10.0']})],
                    {"name": "index", "uni": "main", "id": "dt0", "terms": ["index", "sys", "data"]})
for i in index.d:
    if i.d[2] > last_id:
        last_id = i.d[2]


def newPage(head, body, tags):
    global index, last_id
    tags["id"] = ("idx" + str(last_id + 1))
    index.d.append(object.data([head, body, last_id + 1], tags))
    last_id += 1
    print("added:\nobject.data([\"" + head + "\",\"" + body + "\"," + str(last_id) + "]," + str(tags) + ")")


def readPage(pageId):
    global index
    for i in index.d:
        if i.d[2] == pageId:
            print("    ", i.d[0])
            print("\n", i.d[1])
            print("\nend of entry\n\n", pageId)


def quickRead(pageId):
    global index
    for i in index.d:
        if i.d[2] == pageId:
            for f in i.d[0]:
                print(f)
                sleep(0.2)
            sleep(1)
            for f in i.d[1]:
                print(f)
                sleep(0.2)
            sleep(1)
            # print("\n",i.d[2])
            print("\nend of entry")


def updatePage(head, body, idToModify):
    global index
    for i in index.d:
        if i.d[2] == idToModify:
            if head is not None:
                i.d[0] = head
            if body != None:
                i.d[1] = body


def deletePage(pageId):
    global index
    for i in index.d:
        if i.d[2] == pageId:
            index.d.pop(index(i))


def typer():
    working = True
    terms = []
    title = input("title:\n")
    body = input("body:\n")
    while working:
        i = input("term(type done to stop):\n")
        if i == "done":
            working = False
        else:
            terms.append(i)
    newPage(title, body, {"name": title, "uni": "main", "terms": terms, "id": None})


# runtime
if __name__ == "__main__":
    print("system index v10.0")
    typer()
    readPage(1)
    sleep(2)
    quickRead(1)
