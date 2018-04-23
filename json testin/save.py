# import
import object


# setup
def saveUni(uni, fileName):
    file = open(fileName + ".py", 'w')
    sameBegin = "# AUTO GENERATED CODE\nimport object\ndef load():\n    uni=object.universe("
    variableMiddle = str(uni.tl) + "," + str(uni.scn) + "," + str(uni.obj) + "," + str(uni.cont) + "," + str(
        uni.funct) + "," + str(uni.rule) + "," + str(uni.tag)
    sameEnd = ")\n    return uni\n# END AUTO GENERATED CODE\n# TO USE: IMPORT THIS FILE AND RUN " + fileName + ".load()"
    file.write(sameBegin + variableMiddle + sameEnd)
    file.close()


def saveScn(scn, fileName):
    file = open(fileName + ".py", 'w')
    sameBegin = "# AUTO GENERATED CODE\nimport object\ndef load():\n    scn = object.scene("
    variableMiddle = str(scn.scp) + "," + str(scn.obj) + "," + str(scn.loc) + "," + str(scn.tag)
    sameEnd = ")\n    return scn\n# END AUTO GENERATED CODE\n# TO USE IMPORT THIS FILE AND RUN " + fileName + ".load()"
    file.write(sameBegin + variableMiddle + sameEnd)
    file.close()


def saveScnExe(scn, fileName):
    file = open(fileName + ".py", "w")
    initialVar = ""
    script = ""
    printEnd = "    print("
    for i in scn.obj:
        initialVar += ("    " + i + "\n")
    for i in scn.scp:
        script += ("    " + i + "\n")
    for i in scn.obj:
        objVar = ""
        for f in i:
            if f == " " or f == "=":
                break
            else:
                objVar += f
        printEnd += (objVar + ", ")
    printEnd += "'\\n End')\n"
    fileStart = "# AUTO GENERATED CODE\nimport object\ndef load():\n    scn = object.scene("
    saveScnStr = str(scn.scp) + "," + str(scn.obj) + "," + str(scn.loc) + "," + str(scn.tag)
    saveEndExStart = ")\n    return scn\ndef execute():\n"
    fileEnd = "# END AUTO GENERATED CODE\n# TO USE IMPORT THIS FILE AND RUN " + fileName + ".load()"
    file.write(fileStart + saveScnStr + saveEndExStart + initialVar + script + printEnd + fileEnd)
    file.close()


# outputs the object as a json file
# use: objToJson(<filename>, <obj>)
# requires: obj, space for <filename>.json
def objToJson(filename, obj):
    file = open(filename + ".json", "w")
    mod = '"' + str(obj.mod) + '"'
    trd = '"' + str(obj.trd) + '"'
    tag = '"' + str(obj.tag) + '"'
    json = "{\"mod\":" + mod + ",\"trd\":" + trd + ",\"tag\":" + tag + '}'
    file.write(json)
    file.close()
    print(json, "was saved to", filename + ".json")


# testing
testObj = object.object([[1, "0,0,0-0,0,0"], [1, ["0,0,0", ["0,0,0"], ["0,0,0"]]], [], ["a", [None]]],
                        {"ram": "hello"},
                        {"name": "testObj"})

# runtime
if __name__ == "__main__":
    print("Save v10.0")
    # x = object.scene(["y = 2"], ["y = 1"], "'loc'", "'tag'")
    # saveScnExe(x, "test")
    objToJson("Heyy", testObj)
