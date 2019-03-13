# todo add encryption
# two functions for saving objects to file and getting them from a file
# Module type: prog
import pickle


# saves an sysObject to file
# obj(obj)*, filename(path(str))*
# File creation/ Modification
def saveObj(obj, fileName):
    with open("./"+fileName, 'wb') as out:
        pickle.dump(obj, out, -1)


# load the sysObject at filename
# filename(path(str))*
# obj
def loadObj(fileName):
    with open(fileName, 'rb') as fileData:
        return pickle.load(fileData)


# note: to save multiple objects into one file, save them as a list or a sysh.sysObject.data
#   loadObj() will lo       ad the entire list back, ready for parsing

# Info at run
if __name__ == "__main__":
    print("Two functions for saving objects to file and getting them from a file\nModule type: prog")
