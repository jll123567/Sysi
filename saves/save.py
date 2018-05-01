# import
import object
import json


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
    if isinstance(obj, object.object):
        jsonString = json.dumps({"mod": obj.mod, "trd": obj.trd, "tag": obj.tag})
    elif isinstance(obj, object.user):
        jsonString = json.dumps({"mod": obj.mod, "trd": obj.trd, "prs": obj.prs, "mem": obj.mem, "tag": obj.tag})
    elif isinstance(obj, object.weapon):
        jsonString = json.dumps({"mod": obj.mod, "trd": obj.trd, "dmg": obj.dmg, "tag": obj.tag})
    elif isinstance(obj, object.data):
        jsonString = json.dumps({"d": obj.d, "tag": obj.tag})
    elif isinstance(obj, object.container):
        jsonString = json.dumps({"org": obj.bnd, "bnd": obj.bnd, "tag": obj.tag})
    elif isinstance(obj, object.scene):
        jsonString = json.dumps({"scp": obj.scp, "obj": obj.obj, "loc": obj.loc, "tag": obj.tag})
    elif isinstance(obj, object.universe):
        jsonString = json.dumps({"tl": obj.tl, "scn": obj.scn, "obj": obj.obj, "cont": obj.cont, "funct": obj.funct,
                                 "rule": obj.rule, "tag": obj.tag})
    else:
        raise Exception("File not created, not a system object")
    file.write(jsonString)
    file.close()
    print(jsonString, "was saved to", filename + ".json")


# take the json from <filepath> and returns the object inside
# storageVar = jsonToObj(<filepath>)
# requires: sysh object stored in a json file
def jsonToObj(filepath):
    file = open(filepath, 'r')
    jsonString = file.read()
    jsonString = json.loads(jsonString)
    if "mod" in jsonString:
        if "mem" in jsonString:
            usr = object.user(jsonString["mod"], jsonString["trd"], jsonString["prs"],
                              jsonString["mem"], jsonString["tag"])
            return usr
        elif "dmg" in jsonString:
            wep = object.weapon(jsonString["mod"], jsonString["trd"], jsonString["dmg"], jsonString["tag"])
            return wep
        else:
            obj = object.object(jsonString["mod"], jsonString["trd"], jsonString["tag"])
            return obj
    elif "d" in jsonString:
        dta = object.data(jsonString["d"], jsonString["tag"])
        return dta
    elif "org" in jsonString:
        cont = object.container(jsonString["org"], jsonString["bnd"], jsonString["tag"])
        return cont
    elif "scp" in jsonString:
        scn = object.scene(jsonString["scp"], jsonString["obj"], jsonString["loc"], jsonString["tag"])
        return scn
    else:
        uni = object.universe(jsonString["tl"], jsonString["scn"], jsonString["obj"], jsonString["cont"],
                              jsonString["funct"], jsonString["rule"], jsonString["tag"])
        return uni


# testing
testObj = object.object({"wow": "hello"}, {"also dict": "yep"}, {"name": "testObj"})
testUsr = object.user("i", "am", "full", "of", "string")
testWep = object.weapon(0.1, 0.2, 0.3, 0.5)
testDta = object.data(("huh", "what?"), ("oh", 0, 2))
testCont = object.container([0, 1, 2, 3], ["hi", "bye"], ["so", True])
testScn = object.scene(True, False, True, False)
testUni = object.universe(None, None, None, None, None, None, None)

# runtime
if __name__ == "__main__":
    print("Save v10.0")
    objToJson("Heyy", testObj)
    testObj = None
    testObj = jsonToObj("C:/Users/Jacob Ledbtter/Desktop/code/python/Sysh/json testin/Heyy.json")
    print(testObj.mod)
    objToJson("Heyy", testUsr)
    testUsr = None
    testUsr = jsonToObj("C:/Users/Jacob Ledbtter/Desktop/code/python/Sysh/json testin/Heyy.json")
    print(testUsr.prs)
    objToJson("Heyy", testWep)
    testWep = None
    testWep = jsonToObj("C:/Users/Jacob Ledbtter/Desktop/code/python/Sysh/json testin/Heyy.json")
    print(testWep.dmg)
    objToJson("Heyy", testDta)
    testDta = None
    testDta = jsonToObj("C:/Users/Jacob Ledbtter/Desktop/code/python/Sysh/json testin/Heyy.json")
    print(testDta.d)
    objToJson("Heyy", testCont)
    testCont = None
    testCont = jsonToObj("C:/Users/Jacob Ledbtter/Desktop/code/python/Sysh/json testin/Heyy.json")
    print(testCont.bnd)
    objToJson("Heyy", testScn)
    testScn = None
    testScn = jsonToObj("C:/Users/Jacob Ledbtter/Desktop/code/python/Sysh/json testin/Heyy.json")
    print(testScn.scp)
    objToJson("Heyy", testUni)
    testUni = None
    testUni = jsonToObj("C:/Users/Jacob Ledbtter/Desktop/code/python/Sysh/json testin/Heyy.json")
    print(testUni.rule)
    print("TEST COMPLETE")
    # jasmine Bronte-Marie Williams is the best person i know (i approve this message) ~Jacob Ledbetter
    # JJ/Jasmine/Jazzy is AMAAAZINGGGGGGGG YAYAYAYAYA
