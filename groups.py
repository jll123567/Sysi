# import
import object


# setup
# group is a list of objects
# groupType is a string desc by what objects are in the group (obj,usr,wepcont,scn,uni,dta) + multi for many types
# groupCount is the number of object in the group
# groupSort is a string desc of how the objects are sorted(optional)
# groupRelevance is a string desc of why these objects are grouped(optional)

class group(object.data):
    def __init__(self, storage, tag):
        super(group, self).__init__()
        self.storage = storage
        self.tag = tag

    # adds the groupSort and or groupRelevance tags (None for unused)
    def addOptionalTags(self, groupSort, groupRelevance):
        if groupSort is not None:
            self.tag.update({"groupSort": groupSort})
        if groupRelevance is not None:
            self.tag.update({"groupRelevance": groupRelevance})


# create group with list of elements
def createGroup(objList, groupType, name):
    grp = object.data(objList, {"name": name, "groupType": groupType, "groupCount": len(objList), "id": None})
    return grp


# takes data with a valid group in dta.storage and makes a group
def makeGroup(dta, groupType, name):
    grp = object.data(dta.storage, {"name": name, "groupType": groupType, "groupCount": len(dta.storage), "id": None})
    return grp


# runtime
if __name__ == "__main__":
    print("groups v11.0")
