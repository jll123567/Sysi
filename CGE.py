# The Content Generation engine
# objects in objList are simulated and run based on the instructions in trd.tsk
# Module type: prog
# todo add multiple
# task > CGE
# ["target(obj name)", "operation", [parameters]]
# CGE > sceneScript
# ["sender","target","operation",[parameters]]
import re
import object
import warnings
import prog.idGen as idGen
import threading


# a instance of CGE
# sessionId("str"), objList([obj]), saveScene(scn), uniRules([rule])
class CGESession(threading.Thread):
    def __init__(self, sessionId, objList, saveScene=object.scene(), uniRules=None):
        super().__init__()
        self.sessionId = sessionId
        self.objList = objList
        self.saveScene = saveScene
        if uniRules is None:
            self.uniRules = []
        else:
            self.uniRules = uniRules

    # get the attributes of obj as a list
    # obj(obj)*
    # attributes([str])
    @staticmethod
    def getAttribList(obj):
        objDict = str(obj.__dict__.keys())
        stringList = str(re.search(r"'.*'", objDict).group())
        words = []
        word = ''
        for char in stringList:
            if char == '\'' or char == "\"" or char == ' ':
                continue
            if char == ',':
                words.append(word)
                word = ''
            else:
                word += char
        words.append(word)
        return words

    # get the methods of an object
    # obj(obj)*
    # methodList([str])
    def getMethods(self, obj):
        attribList = self.getAttribList(obj)
        methodList = dir(obj)
        finalList = []
        for method in methodList:
            if method[0] == '_':
                continue
            if method in attribList:
                continue
            finalList.append(method)
        return finalList

    # get the operations that CGE needs to perform this shift
    # none
    # operationList([operations])
    def getOperations(self):
        operationList = []
        for obj in self.objList:
            try:
                for operation in obj.trd.tsk.current:
                    operationList.append(operation)
            except AttributeError:
                warnings.warn(
                    "the object " + str(
                        obj.tag["name"]) + "does not have a threadModules and/or tasker \n please add one "
                                           "if you want the object to do something",
                    objectDoesNotContainTsk)
            for rul in self.uniRules:
                if rul[0] is None:
                    operationList.append([obj.tag["id"], rul[1], rul[2]])
                else:
                    operationList.append([obj.tag["id"] + rul[0], rul[1], rul[2]])
        return operationList

    # resolve the object's id to its position in the objList
    # objectId(str)*
    # index(int)
    def resolveIdToIndex(self, objId):
        # todo: remove this after threading CGE works
        if self.objList.__len__() == 1:
            return 0
        ndx = 0
        for obj in self.objList:
            if objId == obj.tag["id"]:
                break
            ndx += 1
        return ndx

    # returns true if all methods in the operation list are usable on the target object
    # operationList([operation])*
    # operationsPossible(bool)
    def areOperationsPossible(self, operationList):
        for operation in operationList:
            if '.' in operation[0]:
                objId = ""
                ext = ""
                mode = 'n'
                for char in operation[0]:
                    if char == '.' and mode == 'n':
                        mode = '.'
                    if char == '.' and mode == '.':
                        mode = 'e'
                    if mode == 'n':
                        objId += char
                    if mode == 'e':
                        ext += char
                ext = ext[1:]
                methods = self.getMethods(
                    self.unpackSubObjFromExtension(self.objList[self.resolveIdToIndex(objId)], ext))
                if operation[1] not in methods:
                    raise operationNotPossible(str(operation[1]) + " not in " + str(objId + '.' + ext) + " method list")

            else:
                if operation[1] not in self.getMethods(self.objList[self.resolveIdToIndex(operation[0])]):
                    return False
        return True

    # apply the operation to the target object
    # object index(int)*, method to apply(str)*, references to sub objects(str), parameters for the method([any])
    # none
    def performSelectedOperation(self, objIndex, method, subObjectReference=None, parameters=None):
        if parameters is None:
            parameters = []
        if subObjectReference is None:
            if parameters.__len__() == 0:
                try:
                    getattr(self.objList[objIndex], method)()
                except:
                    raise operationNotPossible("getattr(self.objList[objIndex], operation)()")
            else:
                try:
                    getattr(self.objList[objIndex], method)(*parameters)
                except:
                    raise operationNotPossible("getattr(self.objList[objIndex], operation)(*parameters)")
        else:
            # print(objIndex)
            subObj = self.unpackSubObjFromExtension(self.objList[objIndex], subObjectReference)
            if parameters.__len__() == 0:
                try:
                    getattr(subObj, method)()
                except:
                    raise operationNotPossible("getattr(subObj, operation)()")
            else:
                try:
                    getattr(subObj, method)(*parameters)
                except:
                    raise operationNotPossible("getattr(subObj, operation)(*parameters)")
            self.objList[objIndex] = self.repackSubToFull(self.objList[objIndex], subObj, subObjectReference)

    # get a sub object from its extension
    # obj(obj)*, subObjReference(str)*
    # subObj(obj)
    @staticmethod
    def unpackSubObjFromExtension(obj, subObjReference):
        subs = []
        sub = ""
        for char in subObjReference:
            if char == '.':
                subs.append(sub)
                sub = ""
            else:
                sub += char
        subs.append(sub)
        extractedObj = obj
        for subObj in subs:
            extractedObj = getattr(extractedObj, subObj)
        return extractedObj

    # take an updated subObj and put it into the original obj
    # fullObj(obj)*, subObj(obj)*, subObjReference(str)*
    # fullObj(obj)
    @staticmethod
    def repackSubToFull(fullObj, subObj, subObjReference):
        subs = []
        sub = ""
        for char in subObjReference:
            if char == '.':
                subs.append(sub)
                sub = ""
            else:
                sub += char
        subs.append(sub)
        currentSub = subs[-1]
        subs.pop(-1)

        while subs:
            extractedObj = fullObj
            for subObjs in subs:
                extractedObj = getattr(extractedObj, subObjs)
            setattr(extractedObj, currentSub, subObj)
            subObj = extractedObj
            currentSub = subs[-1]
            subs.pop(-1)
        setattr(fullObj, currentSub, subObj)
        return fullObj

    # preps the objList for the next shift
    # none
    # none
    def moveThreadAlong(self):
        objsEmpty = 0
        for obj in self.objList:
            if obj.trd.tsk.profile.__len__() == 0:
                objsEmpty = 0
            try:
                obj.trd.tsk.nextCurrent()
            except AttributeError:
                pass
        print("shift completed")
        if objsEmpty == self.objList.__len__():
            print("all object's threads empty \ndumping objects from list")
            self.objList = []

    # adds obj to the objList
    # obj(obj)*
    # none
    def addObj(self, obj):
        self.objList.append(obj)

    # add universe rules
    # uni(uni)*
    # none
    def addUniRules(self, uni):
        for rul in uni.rule:
            self.uniRules.append(rul)

    # save the state of the objList as the initial state of a scene, with optional container setting
    # cont(container)
    # none
    def saveSceneInit(self, cont=None):
        if cont is not None:
            self.saveScene.loc = cont
        self.saveScene.obj = self.objList

    # get the finished scene recording
    # timeLine information([str])*, scene name(str)*, universe to gen id(uni)*
    # scene(scene)
    def exportScene(self, tlInfo, name, universe):
        self.saveScene.scp[0] = tlInfo
        self.saveScene.tag["name"] = name
        self.saveScene.tag["id"] = idGen.generateUniversalId(universe, self.saveScene)
        return self.saveScene

    # update the objects in objList based on obj Thread
    # saveToScene(bool)
    # no object message(str)/None
    def update(self, saveToScene=False):
        if not self.objList:
            return "No objects to process"
        objIdx = 0
        for _ in self.objList:
            if not self.objList[objIdx].trd.tsk.current:
                continue
            if not isinstance(self.objList[objIdx].trd.tsk.current[0], list):
                self.objList[objIdx].trd.tsk.current[0] = [self.objList[objIdx].trd.tsk.current[0]]
            objIdx += 1
        operationList = self.getOperations()
        # if not
        self.areOperationsPossible(operationList)
        # raise operationNotPossible(operationList)
        if saveToScene:
            self.saveScene.scp.append(operationList)
        for op in operationList:
            objId = ""
            ext = ""
            mode = 'n'
            if '.' in op[0]:
                for char in op[0]:
                    if char == '.' and mode == 'n':
                        mode = '.'
                    if char == '.' and mode == '.':
                        mode = 'e'
                    if mode == 'n':
                        objId += char
                    if mode == 'e':
                        ext += char
                if ext == "":
                    ext = None
                else:
                    ext = ext[1:]
                pass
            if ext == "":
                objId = op[0]
                # print("pso: ", name)
                self.performSelectedOperation(self.resolveIdToIndex(objId), op[1], None, op[2])
            else:
                self.performSelectedOperation(self.resolveIdToIndex(objId), op[1], ext, op[2])
            if "evLog" in self.objList[self.resolveIdToIndex(objId)].tag.keys():
                self.objList[self.resolveIdToIndex(objId)].tag["evLog"].append(op[1])
            else:
                self.objList[self.resolveIdToIndex(objId)].tag.update({"evLog": [op[1]]})

        self.moveThreadAlong()

    # threading.thread objects need a run
    # todo make the run better
    # iterations(int>0)
    # none
    def run(self, iterations=1000):
        while iterations > 0:
            self.update()
            iterations -= 1

    # update the objList while a boolean expression is true
    # id of obj to check against(int)*, comparator(str)*, goal(any)*, saveToScene(bool), subObjReference(str)
    # none/console output(str)
    def updateWithGoal(self, objId, comparator, goal, subObjReference=None, saveToScene=False):
        if subObjReference is not None:
            test = self.unpackSubObjFromExtension(self.resolveIdToIndex(objId), subObjReference)
            del test
        if subObjReference is None:
            while goal != self.resolveIdToIndex(objId):
                self.update(saveToScene)
        elif comparator == '==':
            while goal != self.unpackSubObjFromExtension(self.resolveIdToIndex(objId), subObjReference):
                self.update(saveToScene)
        elif comparator == '!=':
            while goal == self.unpackSubObjFromExtension(self.resolveIdToIndex(objId), subObjReference):
                self.update(saveToScene)
        elif comparator == '>':
            while goal <= self.unpackSubObjFromExtension(self.resolveIdToIndex(objId), subObjReference):
                self.update(saveToScene)
        elif comparator == '<':
            while goal >= self.unpackSubObjFromExtension(self.resolveIdToIndex(objId), subObjReference):
                self.update(saveToScene)
        elif comparator == '>=':
            while goal < self.unpackSubObjFromExtension(self.resolveIdToIndex(objId), subObjReference):
                self.update(saveToScene)
        elif comparator == '<=':
            while goal != self.unpackSubObjFromExtension(self.resolveIdToIndex(objId), subObjReference):
                self.update(saveToScene)
        else:
            print("the comparator inputted is not valid")

    # replay a scene from start shift to last shift
    # scn.scp[1:lastShift] none being [1:]
    # scene to replay(scn)*, last shift(none or int)
    # scene objs [obj]
    def replayScene(self, scn, lastShift=None):
        self.objList = scn.obj
        if lastShift is None:
            script = scn.scp[1:]
        else:
            script = scn.scp[1:lastShift]
        print(script)
        for shift in script:
            if not self.objList:
                return "No objects to process"
            self.areOperationsPossible(shift)
            for operation in shift:
                objId = ""
                ext = ""
                mode = 'n'
                if '.' in operation[0]:
                    for char in operation[0]:
                        if char == '.' and mode == 'n':
                            mode = '.'
                        if char == '.' and mode == '.':
                            mode = 'e'
                        if mode == 'n':
                            objId += char
                        if mode == 'e':
                            ext += char
                    if ext == "":
                        ext = None
                    else:
                        ext = ext[1:]
                    pass
                if ext == "":
                    objId = operation[0]
                    self.performSelectedOperation(self.resolveIdToIndex(objId), operation[1], None, operation[2])
                else:
                    self.performSelectedOperation(self.resolveIdToIndex(objId), operation[1], ext, operation[2])
        scn.obj = self.objList
        self.objList = []
        return scn.obj


# warning if the an operation is not possible as listed
# expression(warning.expression)*, message(str)
class operationNotPossible(Exception):
    def __init__(self, expression, message="one or more operations are not available as writen"):
        self.expression = expression
        self.message = message


# warning if an object doesn't have a trd.tsk
# None
class objectDoesNotContainTsk(Warning):
    pass


# Info at run
if __name__ == "__main__":
    print("The Content Generation engine\nobjects in objList are simulated and run based on the instructions in "
          "trd.tsk\nModule type: prog")
