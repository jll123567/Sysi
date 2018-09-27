# a small bug tracker like thing
# module type: prog


# error queue(fill with err
queue = []


# queues and resolves a list of errors
# errs([err])*
# Console output(str)
def errorQueue(errs):
    global queue
    for err in errs:
        print(str(len(queue)) + " left to resolve")
        err.resolveError()
    print("queue empty exiting")


# info at run
if __name__ == "__main__":
    print("a small bug tracker like thing\nmodule type: prog")
