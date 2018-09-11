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
        print(str(len(queue)) + " left to resolve")
        i.resolveError()
    print("queue empty exiting")


# runtime
if __name__ == "__main__":
    print("ready\nawaiting errorQueus(errs) call")
