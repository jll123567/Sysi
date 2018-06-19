# import
import object


# setup
# group is a list of objects
# groupType is a string desc by what objects are in the group (obj,usr,wepcont,scn,uni,dta) + multi for many types
# groupCount is the number of object in the group
# groupSort is a string desc of how the objects are sorted(optional)
# groupRelevance is a string desc of why these objects are grouped(optional)

# create group with list of elements
def createGroup(objList, groupType, name):
    grp = object.data(objList, {"name": name, "groupType": groupType, "groupCount": len(objList)})
    return grp


# takes data with a valid group in dta.storage and makes a group
def makeGroup(dta, groupType, name):
    grp = object.data(dta.storage, {"name": name, "groupType": groupType, "groupCount": len(dta.storage)})
    return grp


# adds the groupSort and or groupRelevance tags (None for unused)
def addOptionalTags(grp, groupSort, groupRelevance):
    if groupSort is not None:
        grp.tag.update({"groupSort": groupSort})
    if groupRelevance is not None:
        grp.tag.update({"groupRelevance": groupRelevance})
    return grp


# runtime
if __name__ == "__main__":
    print("groups v11.0")
