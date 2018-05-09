# import
import error

# setup
# a small bug tracker like thing(idk)
# errorQueue(array of errors)
# addToQueue(err)

queue = []


def errorQueue(errs):
    global queue
    for i in errs:
        queue.append(i)
    for i in queue:
        print(str(len(queue)) + " left to resolve")
        error.resolveError(i)
    print("queue empty exiting")


# runtime
if __name__ == "__main__":
    print("ready\nawaiting errorQueus(errs) call")
