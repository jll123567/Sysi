# definitions for some data types
# module type: std


# adds type tags
# dta(dta)*
# updatedDta(dta)*
def addTypeTags(dta):
    dta.tag.update({"dataType": ""})
    return dta


# sets the data type tag
# use the following or just do dta.tag["dataType"] = <string>
# dta(dta)*, dataType(str)*
# updatedDta(dta)
def setType(dta, dataType):
    dta.tag["dataType"] = str(dataType)
    return dta


# undoes the type tag
# dta(dta)*
# updatedDta(dta)
def removeTypeTags(dta):
    del dta.tag["dataType"]
    return dta


# Info at run
if __name__ == "__main__":
    print("definitions for some data types\nmodule type: std")
