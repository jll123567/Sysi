# import
# from time import sleep
import object

# setup
# format:
# dta([head,body,id],tags)
index = object.data([object.data(["Hello, world!", "sysh V11.0 is here. :D", 0],
                                 {'name': 'Hello, world!', 'terms': ['sys', 'Hello,world!', 'v11.0'], "id": None})],
                    {"name": "index"})


def newPage(head, body, pageTags):
    global index
    pageId = 0
    for page in index.storage:
        if page.storage[2] > pageId:
            pageId = page.storage[2]
    pageId += 1
    pageTags["id"] = ("idx" + str(pageId))
    index.storage.append(object.data([head, body, pageId], pageTags))
    print("added:\nobject.data([\"" + head + "\",\"" + body + "\"," + str(pageId) + "]," + str(pageTags) + ")")


def readPage(pageId):
    global index
    for i in index.storage:
        if i.storage[2] == pageId:
            print(i.storage[0])
            print("\n   ", i.storage[1])
            print("\nend of entry\n\n", pageId)


# def quickRead(pageId):
#     global index
#     for i in index.storage:
#         if i.storage[2] == pageId:
#             for f in i.storage[0]:
#                 print(f)
#                 sleep(0.2)
#             sleep(1)
#             for f in i.storage[1]:
#                 print(f)
#                 sleep(0.2)
#             sleep(1)
#             # print("\n",i.storage[2])
#             print("\n end of entry")

# what was I even using this for???


def updatePage(head, body, terms, idToModify):
    global index
    for i in index.storage:
        if i.storage[2] == idToModify:
            if head is not None:
                i.storage[0] = head
            if body is not None:
                i.storage[1] = body
            if terms is not None:
                i.tag["terms"] = terms


def deletePage(pageId):
    global index
    for i in index.storage:
        if i.storage[2] == pageId:
            index.storage.pop(index(i))


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
    print("system index v11.0")
