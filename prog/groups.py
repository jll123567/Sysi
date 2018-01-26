# import
import object


# setup
# group is a list of objects
# groupType is a string desc by what objects are in the group (obj,usr,wep,dev,cont,scn,uni,dta) + multi for many types
# groupCount is the number of object in the group
# groupSort is a string desc of how the objects are sorted(optional)
# groupRelevance is a string desc of why these objects are grouped(optional)

# create group with list of elements
def createGroup(objList, groupType, name):
    grp = object.data(objList, {"name": name, "groupType": groupType, "groupCount": len(objList)})
    return grp


# takes data with a valid group in dta.d and makes a group
def makeGroup(dta, groupType, name):
    grp = object.data(dta.d, {"name": name, "groupType": groupType, "groupCount": len(dta.d)})
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
    print("groups v10.0")
