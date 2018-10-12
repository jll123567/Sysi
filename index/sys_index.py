# a set of pages for what sys is and how to use it, along with functions for adding more pages
# module type: prog
# from time import sleep
import object

# index page format:
# dta([head,body,id],tags)


# storage object for pages
index = object.data([object.data(["Hello, world!", "sysh V11.0 is here. :D", 0],
                                 {'name': 'Hello, world!', 'terms': ['sys', 'Hello,world!', 'v11.0'], "id": None})],
                    {"name": "index"})


# create a new page
# head(str)*, body(str)*, terms(list)*
# Console Output(str)
def newPage(head, body, terms):
    global index
    pageId = 0
    for page in index.storage:
        if page.storage[2] > pageId:
            pageId = page.storage[2]
    pageId += 1
    page = object.data([head, body, pageId], None)
    page.tag.update({"id": ("idx" + str(pageId)), "terms": terms, "name": head})
    index.storage.append(page)
    print("added:\nobject.data([\"" + head + "\",\"" + body + "\"," + str(pageId) + "]," + str(page.tag) + ")")


# prints the page with pageId to the console
# pageId(int)*
# Console Output(str)
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


# change information of a page
# head(str)*, body(str)*, terms(list)*, idToModify(int)*
# none
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


# remove the page
# pageId(int)*
# none
def deletePage(pageId):
    global index
    for i in index.storage:
        if i.storage[2] == pageId:
            index.storage.pop(index(i))


# small typing thing
# input()
# Console Output(str)
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


# info at run
if __name__ == "__main__":
    print("A set of pages for what sys is and how to use it, along with functions for adding more pages\nmodule type: "
          "prog")
