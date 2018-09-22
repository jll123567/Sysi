# setup
# a small bug tracker like thing(idk)
# errorQueue(array of errors)
# addToQueue(err)

queue = []


def errorQueue(errs):
    global queue
    for err in errs:
        print(str(len(queue)) + " left to resolve")
        err.resolveError()
    print("queue empty exiting")


# runtime
if __name__ == "__main__":
    print("ready\nawaiting errorQueues(errs) call")
