# import
import object
import json


# setup
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
        jsonString = json.dumps({"storage": obj.storage, "tag": obj.tag})
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
        dta = object.data(jsonString["storage"], jsonString["tag"])
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
