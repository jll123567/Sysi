# obj groups
# module type: def/std
import sys_objects

# group is a list of objects
# groupType is a string desc by what objects are in the group (obj,usr,wep,cont,scn,uni,dta) + multi for many types
# groupSort is a string desc of how the objects are sorted(optional)
# groupRelevance is a string desc of why these objects are grouped(optional)


class group(sys_objects.data):

    # adds the groupSort and or groupRelevance tags (None for unused)
    # groupSort(groupSort tag)*, groupRelevance(groupRelevance)*
    # none
    def addOptionalTags(self, groupSort, groupRelevance):
        if groupSort is not None:
            self.tag.update({"groupSort": groupSort})
        if groupRelevance is not None:
            self.tag.update({"groupRelevance": groupRelevance})


# create group with list of elements
# objList([obj])*, groupType(str)*, name(str)*
# grp(group)
def createGroup(objList, groupType, name):
    grp = sys_objects.data(objList, {"name": name, "groupType": groupType, "id": None})
    return grp


# takes data with a valid group in dta.storage and makes a group
# dta(valid Grp Dta)*, groupType(str)*, name(str)*
# grp(group
def makeGroup(dta, groupType, name):
    grp = sys_objects.data(dta.storage, {"name": name, "groupType": groupType, "id": None})
    return grp


# runtime
if __name__ == "__main__":
    print("obj groups\nmodule type: def/std")
