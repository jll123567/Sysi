# import
import pickle


def saveObj(obj, fileName):
    with open(fileName, 'wb') as out:
        pickle.dump(obj, out, -1)


def loadObj(fileName):
    with open(fileName, 'rb') as fileData:
        return pickle.load(fileData)


# note: to save multiple objects into one file, save them as a list or a sysh.object.data
#   loadObj() will load the entire list back to be ready to parse it

# runtime
if __name__ == "__main__":
    print("Save v11.0")
