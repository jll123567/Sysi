# A function to dump the contents of objects
# Needs improvement
# module type: prog


# dumps the stuff in an object
# obj(any)*
# console output(str)
def dumpObject(obj):
    for data in obj.__dict__():
            print(data)


if __name__ == "__main__":
    print("A function to dump the contents of objects\nmodule type: prog")
