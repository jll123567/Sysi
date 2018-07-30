##ADMIN TOOL##

# setup
def addTypeTags(dta):
    dta.tag.update({"dataType": ""})
    return dta


# use the following or just do dta.tag["dataType"] = <string>
def setType(dta, dataType):
    dta.tag["dataType"] = str(dataType)
    return dta


def removeTypeTags(dta):
    del dta.tag["dataType"]
    return dta


# runtime
if __name__ == "__main__":
    print("data types tags v10.0")
