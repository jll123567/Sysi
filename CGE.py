# The Content Generation engine
# objects in objList are simulated and run based on the instructions in trd.tsk
# Module type: prog
# task > CGE
# ["target(obj name)", "operation", [parameters]]
# CGE > sceneScript
# ["sender","target","operation",[parameters]]
import re
import object
import warnings
import prog.idGen as idGen
import threading


class CrossSessionHandler(threading.Thread):
    """"""

    def __init__(self, CSHId, sessionList=None):
        super().__init__()
        if sessionList is None:
            self.sessionList = []
        else:
            self.sessionList = sessionList
        self.CSHId = CSHId

    def addSession(self, session):
        self.sessionList.append(session)

    def checkForPost(self):
        for session in self.sessionList:
            if session.crossPosts:
                self.pendSessions()
                self.resolvePosts()
                self.unpendSessions()

    def pendSessions(self):
        for idx in range(0, self.sessionList.__len__()):
            self.sessionList[idx].crossPosts.append("pend")

    def unpendSessions(self):
        for idx in range(0, self.sessionList.__len__()):
            for idx1 in range(0, self.sessionList[idx].crossPosts.__len__()):
                if self.sessionList[idx].crossPosts[idx1] == "pend":
                    self.sessionList[idx].crossPosts.pop(idx1)

    def resolvePosts(self):
        objToRes = None
        for idx in range(0, self.sessionList.__len__()):
            for post in self.sessionList[idx].crossPosts:
                if post == "pend":
                    continue
                else:
                    for obj in self.sessionList[idx].objList:
                        if obj.tag["id"] == post:
                            objToRes = obj
                    for operation in objToRes.trd.tsk.current:
                        if operation[1] == "crossWarp":
                            # set True when the target session has and object with the same id as the objToRes
                            testVar = False
                            for idx1 in range(0, self.sessionList.__len__()):
                                if self.sessionList[idx1] == operation[2][0]:
                                    for idx2 in range(0, self.sessionList[idx1].objList.__len__()):
                                        if self.sessionList[idx1].objList.objList[idx2].tag["id"] == objToRes.tag["id"]:
                                            self.sessionList[idx1].load(objToRes.tag["id"], objToRes.mod, objToRes.trd,
                                                                        None, objToRes.tag)
                                            self.sessionList[idx].unload(objToRes.tag["id"])
                                            testVar = True
                                            break
                                    if not testVar:
                                        self.sessionList[idx1].addObj(objToRes)
                                        self.sessionList[idx].unload(objToRes.tag["id"])
                                    break
                        else:
                            print("operation not supported")
                        break
                    self.sessionList[idx].crossPosts.pop(self.sessionList[idx].crossPosts.index(post))

    def run(self):
        while True:
            self.checkForPost()


class CGESession(threading.Thread):
    """an instance of CGE
    sessionID is a string
    objList is a list of objects
    run behavior is a list where index 0 is a single character string t, g or i
        't'ill tsk's empty
        till 'g'oal met([])
        till all 'i'terations completed([])
    saveScene is a scene to save to
    uniRules is a list of tsk operations to run each shift"""

    def __init__(self, sessionId, objList, runBehavior, savedScene=object.scene(), crossPosts=None, uniRules=None):
        """initialize attributes
        superclass:threading.thread
        savedScene: an empty scene
        uniRules: None"""
        super().__init__()
        self.sessionId = sessionId
        self.objList = objList
        self.runBehavior = runBehavior
        self.savedScene = savedScene
        if uniRules is None:
            self.uniRules = []
        else:
            self.uniRules = uniRules
        if crossPosts is None:
            self.crossPosts = []
        else:
            self.crossPosts = crossPosts

    def unload(self, objId):
        """sets model and thread or storage of the object in objList with objId to None
        only use after object has been copied to another session to avoid data loss"""
        unload = self.objList[self.resolveIdToIndex(objId)]
        try:
            # noinspection PyUnusedLocal
            test = unload.mod
            test = unload.trd
            del test
        except AttributeError:
            try:
                test = unload.storage
                del test
            except AttributeError:
                print("Cannot unload. Object does not have a trd, storage or mod")

            else:
                unload.storage = None
        else:
            unload.mod = None
            unload.trd = None
        self.objList[self.resolveIdToIndex(objId)] = unload

    def load(self, objId, modNew=None, trdNew=None, storageNew=None, tagNew=None):
        """loads a mod and trd or storage into the object at objList with objId
        should be called before the object in its origin session is unloaded
        if the object is not in the target session's object list use addObj() instead"""
        loading = self.objList[self.resolveIdToIndex(objId)]
        try:
            # noinspection PyUnusedLocal
            test = loading.mod
            test = loading.trd
            del test
        except AttributeError:
            try:
                test = loading.storage
                del test
            except AttributeError:
                print("Cannot loading. Object does not have a trd, storage or mod")

            else:
                loading.storage = storageNew
        else:
            loading.mod = modNew
            loading.trd = trdNew
        loading.tag = tagNew
        self.objList[self.resolveIdToIndex(objId)] = loading

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
        """checks if operations in operationList are possible by seeing if there is the requested method at the
            requested object
        returns True if all operations have usable methods
        raises operationNotPossible otherwise"""
        for operation in operationList:
            if operation[0] == "CSH":
                if operation[1] == "crossWarp":
                    continue
                else:
                    return False
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
                    raise operationNotPossible(str(operation[1]) + " not in " + str(objId + '.' + ext) + "'s method "
                                                                                                         "list")

            else:
                if operation[1] not in self.getMethods(self.objList[self.resolveIdToIndex(operation[0])]):
                    raise operationNotPossible(str(operation[1]) + "not in" + str(operation[0]) + "'s method list")
        return True

    # apply the operation to the target object
    # object index(int)*, method to apply(str)*, references to sub objects(str), parameters for the method([any])
    # none
    def performSelectedOperation(self, objIndex, method, sourceId, subObjectReference=None, parameters=None):
        if parameters is None:
            parameters = []
        if objIndex == "CSH":
            self.crossPosts.append(sourceId)
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
        while True:
            if not self.crossPosts:
                break
        objsEmpty = 0
        for obj in self.objList:
            if obj.trd.tsk.profile.__len__() == 0:
                objsEmpty = 0
            try:
                obj.trd.tsk.nextCurrent()
            except AttributeError:
                pass
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
            self.savedScene.loc = cont
        self.savedScene.obj = self.objList

    # get the finished scene recording
    # timeLine information([str])*, scene name(str)*, universe to gen id(uni)*
    # scene(scene)
    def exportScene(self, tlInfo, name, universe):
        self.savedScene.scp[0] = tlInfo
        self.savedScene.tag["name"] = name
        self.savedScene.tag["id"] = idGen.generateUniversalId(universe, self.savedScene)
        return self.savedScene

    # update the objects in objList based on obj Thread
    # saveToScene(bool)
    # no object message(str)/None
    def update(self, saveToScene=False):
        if not self.objList:
            return "No objects to process"
        objIdx = 0
        for _ in self.objList:
            if self.objList[objIdx].trd is None:
                continue
            if not self.objList[objIdx].trd.tsk.current:
                continue
            if not isinstance(self.objList[objIdx].trd.tsk.current[0], list):
                self.objList[objIdx].trd.tsk.current[0] = [self.objList[objIdx].trd.tsk.current[0]]
            objIdx += 1
        operationList = self.getOperations()
        self.areOperationsPossible(operationList)
        if saveToScene:
            self.savedScene.scp.append(operationList)
        if not operationList:
            return "No operations"
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
                self.performSelectedOperation(self.resolveIdToIndex(objId), op[1], op[3], None, op[2])
            else:
                self.performSelectedOperation(self.resolveIdToIndex(objId), op[1], op[3], ext, op[2])
            if "evLog" in self.objList[self.resolveIdToIndex(objId)].tag.keys():
                self.objList[self.resolveIdToIndex(objId)].tag["evLog"].append(op[1])
            else:
                self.objList[self.resolveIdToIndex(objId)].tag.update({"evLog": [op[1]]})

        self.moveThreadAlong()
        return "Shift Complete"

    # threading.thread objects need a run
    # iterations(int>0)
    # none
    def run(self):
        if self.runBehavior[0] == 't':
            while self.update(self.runBehavior[1]) != "No operations":
                pass
            print("No operations left to preform\nstopping!")
        elif self.runBehavior[0] == 'g':
            self.updateWithGoal(self.runBehavior[2], self.runBehavior[3], self.runBehavior[4], self.runBehavior[1],
                                self.runBehavior[5])
        elif self.runBehavior[0] == 'i':
            initialIterCount = self.runBehavior[2]
            while self.runBehavior[2] > 0:
                self.update(self.runBehavior[1])
                print("iteration " + str(initialIterCount - self.runBehavior[2]) + " completed")
                self.runBehavior[2] -= 1
        else:
            return "specify a mode"

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
                targetObjId = ""
                ext = ""
                mode = 'n'
                if '.' in operation[0]:
                    for char in operation[0]:
                        if char == '.' and mode == 'n':
                            mode = '.'
                        if char == '.' and mode == '.':
                            mode = 'e'
                        if mode == 'n':
                            targetObjId += char
                        if mode == 'e':
                            ext += char
                    if ext == "":
                        ext = None
                    else:
                        ext = ext[1:]
                    pass
                if ext == "":
                    targetObjId = operation[0]
                    self.performSelectedOperation(self.resolveIdToIndex(targetObjId), operation[1], operation[3], None,
                                                  operation[2])
                else:
                    self.performSelectedOperation(self.resolveIdToIndex(targetObjId), operation[1], operation[3], ext,
                                                  operation[2])
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
