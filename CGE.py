"""The Content Generation engine
objects in objList are simulated and run based on the instructions in trd.tsk
Module type: prog
task > CGE
["target(obj name)", "operation", [parameters]]
CGE > sceneScript
["sender","target","operation",[parameters]]"""
import re
import object
import warnings
import prog.idGen as idGen
import threading


class CrossSessionHandler(threading.Thread):
    """holds all relevant sessions and allows for data and objects to travel across sessions
    may be refereed to as a "session directory"
    sessionList is a list of CGESessions"""

    def __init__(self, CSHId, sessionList=None):
        """sessionList: []"""
        super().__init__()
        if sessionList is None:
            self.sessionList = []
        else:
            self.sessionList = sessionList
        self.CSHId = CSHId

    def addSession(self, session):
        """add session to self.sessionList"""
        self.sessionList.append(session)

    def checkForPost(self):
        """look for cross session posts(cross post) in each session"""
        for session in self.sessionList:
            if session.crossPosts:
                self.pendSessions()
                self.resolvePosts()
                self.unpendSessions()

    def pendSessions(self):
        """put a cross post telling CSH to not process any more cross posts"""
        for idx in range(0, self.sessionList.__len__()):
            self.sessionList[idx].crossPosts.append("pend")

    def unpendSessions(self):
        """remove the pending cross post"""
        for idx in range(0, self.sessionList.__len__()):
            for idx1 in range(0, self.sessionList[idx].crossPosts.__len__()):
                if self.sessionList[idx].crossPosts[idx1] == "pend":
                    self.sessionList[idx].crossPosts.pop(idx1)

    def resolvePosts(self):
        """parse posts for things for CSH to do, then do those things"""
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
                            self.crossWarp(idx, operation)
                        else:
                            print("operation not supported")
                        break
                    self.sessionList[idx].crossPosts.pop(self.sessionList[idx].crossPosts.index(post))

    def crossWarp(self, idx, operation):
        for idx1 in range(0, self.sessionList.__len__()):
            if self.sessionList[idx1].sessionId == operation[2][0]:
                self.sessionList[idx1].addObj(self.sessionList[idx].objList[
                                                  self.sessionList[idx].resolveIdToIndex(
                                                      operation[3])])
                self.sessionList[idx].removeObj(operation[3])

    # use .start() NOT .run()
    def run(self):
        """obligatory Thread.run
        starts all session threads and  indefinitely, continually, calls checkForPost()"""
        for idx in range(0, self.sessionList.__len__()):
            self.sessionList[idx].start()
        while True:
            self.checkForPost()


class CGESession(threading.Thread):
    """an instance of CGE
    sessionID is a string
    objList is a list of objects
    run behavior is a list where index 0 is a single character string t, g or i
        run update 'c'ontinuealy
        run update until 'g'oal met
        run update until all 'i'terations completed
    saveScene is a scene to save to
    crossPosts is a list holding each cross post
    uniRules is a list of tsk operations to run each shift"""

    def __init__(self, sessionId, objList, runBehavior, savedScene=None, crossPosts=None, uniRules=None):
        """savedScene: an empty scene
        uniRules: []
        crossPosts: []"""
        super().__init__()
        self.sessionId = sessionId
        self.objList = objList
        self.runBehavior = runBehavior
        if savedScene is None:
            self.savedScene = object.scene()
        else:
            self.savedScene = savedScene
        if uniRules is None:
            self.uniRules = []
        else:
            self.uniRules = uniRules
        if crossPosts is None:
            self.crossPosts = []
        else:
            self.crossPosts = crossPosts

    def removeObj(self, objId):
        """removes the sysObject with objId from self.objList
        only use after sysObject has been copied to another session to avoid data loss
        this operation is saved """
        try:
            self.objList.pop(self.resolveIdToIndex(objId))
            if self.savedScene is not None:
                self.savedScene.scp.append(["this", "removeObj", [objId], "this"])
        except objectNotInObjList:
            pass

    def addObj(self, obj):
        """add obj to self.objList"""
        self.objList.append(obj)
        if self.savedScene is not None:
            self.savedScene.scp.append(["this", "addObj", [obj], "this"])

    @staticmethod
    def getAttribList(obj):
        """get a list of the attributes of obj"""
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

    def getMethods(self, obj):
        """get a list of all methods of obj"""
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

    def getOperations(self):
        """get all operations from trd.tsk of all objects in self.objectList"""
        operationList = []
        for obj in self.objList:
            try:
                for operation in obj.trd.tsk.current:
                    operationList.append(operation)
            except AttributeError:
                warnings.warn(
                    "the sysObject " + str(
                        obj.tag["name"]) + "does not have a thread_modules and/or tasker \n please add one "
                                           "if you want the sysObject to do something",
                    objectDoesNotContainTsk)
            for rul in self.uniRules:
                if rul[0] is None:
                    operationList.append([obj.tag["id"], rul[1], rul[2], rul[3]])
                else:
                    operationList.append([obj.tag["id"] + rul[0], rul[1], rul[2], rul[3]])
        return operationList

    def resolveIdToIndex(self, objId):
        """get the index in self.objectList of the sysObject with the id, objId"""
        if self.objList.__len__() == 1:
            return 0
        ndx = 0
        for obj in self.objList:
            if objId == obj.tag["id"]:
                return ndx
            ndx += 1
        raise objectNotInObjList(objId)

    def areOperationsPossible(self, operationList):
        """checks if operations in operationList are possible by seeing if there is the requested method at the
            requested sysObject
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

    def performSelectedOperation(self, objId, method, sourceId, subObjectReference=None, parameters=None):
        """checks if the sysObject with an id of sourceId can request method
        if yes, method(parameters), is call to the sysObject in the objList with the id of objId or it's sub sysObject
        otherwise raise operationNotPossible"""
        if parameters is None:
            parameters = []
        if objId == "CSH":
            self.crossPosts.append(sourceId)

        elif objId == "this":
            if parameters.__len__() == 0:
                try:
                    getattr(self, method)()
                except:
                    raise operationNotPossible("this, " + method)
            else:
                try:
                    getattr(self, method)(*parameters)
                except:
                    raise operationNotPossible("this, " + method + ',' + parameters)

        elif subObjectReference is None:
            if parameters.__len__() == 0:
                try:
                    getattr(self.objList[self.resolveIdToIndex(objId)], method)()
                except:
                    raise operationNotPossible(objId + ',' + method + ',' + parameters)
            else:
                try:
                    getattr(self.objList[self.resolveIdToIndex(objId)], method)(*parameters)
                except:
                    raise operationNotPossible(objId + ',' + method + ',' + parameters)
        else:
            subObj = self.unpackSubObjFromExtension(self.objList[self.resolveIdToIndex(objId)], subObjectReference)
            if parameters.__len__() == 0:
                try:
                    getattr(subObj, method)()
                except:
                    raise operationNotPossible(objId + ',' + method)
            else:
                try:
                    getattr(subObj, method)(*parameters)
                except:
                    raise operationNotPossible(objId + ',' + method + ',' + parameters)
            self.objList[self.resolveIdToIndex(objId)] = self.repackSubToFull(
                self.objList[self.resolveIdToIndex(objId)], subObj, subObjectReference)

    @staticmethod
    def unpackSubObjFromExtension(obj, subObjReference):
        """get the sub sysObject, referenced by subObReference, of obj"""
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

    @staticmethod
    def extractId(operation):
        """takes an operation and gives back a list with the target sysObject id and the sub-sysObject reference if any"""
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
        return [objId, ext]

    @staticmethod
    def repackSubToFull(fullObj, subObj, subObjReference):
        """return fullObj with its sub sysObject, referenced by subObjReference, equal to subObj"""
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

    def moveThreadAlong(self):
        """move trd of all objects in self.objList to next shift"""
        while True:
            if not self.crossPosts:
                break
        objsEmpty = 0
        for idx in range(0, self.objList.__len__()):
            if self.objList[idx].trd.tsk.profile.__len__() == 0:
                objsEmpty += 1
                continue
            try:
                self.objList[idx].trd.tsk.nextCurrent()
            except AttributeError:
                pass
        if objsEmpty == self.objList.__len__():
            self.objList = []

    def addUniRules(self, uni):
        """add a rule to  self.uniRules"""
        for rul in uni.rule:
            self.uniRules.append(rul)

    def saveSceneInit(self, cont=None):
        """save the current state of the session as the initial state of self.saveScene"""
        if cont is not None:
            self.savedScene.loc = cont
        self.savedScene.obj = self.objList

    def exportScene(self, tlInfo, name, universe):
        """export self.savedScene with timeline info from tlInfo, the scene name from name,
         and an Id generated with universe"""
        self.savedScene.scp[0] = tlInfo
        self.savedScene.tag["name"] = name
        self.savedScene.tag["id"] = idGen.generateUniversalId(universe, self.savedScene)
        return self.savedScene

    def update(self, saveToScene=False):
        """extract and operate on objects in self.objectList using the operations from the threads of said objects
        may return a string if an issue occurred or something unexpected happened"""
        if not self.objList:
            return "No objects to process"
        objIdx = 0
        # check if sysObject has a thread and a tasker and the trd.tsk.current[0] is a list
        for _ in self.objList:
            if self.objList[objIdx].trd is None:
                # replace me to debug
                continue
            if not self.objList[objIdx].trd.tsk.current:
                # replace me to debug
                continue
            if not isinstance(self.objList[objIdx].trd.tsk.current[0], list):
                # I just fix crappy tsk code
                self.objList[objIdx].trd.tsk.current[0] = [self.objList[objIdx].trd.tsk.current[0]]
            objIdx += 1
        operationList = self.getOperations()
        self.areOperationsPossible(operationList)
        if saveToScene:
            self.savedScene.scp.append(operationList)
        if not operationList:
            return "No operations"

        for op in operationList:
            idHold = self.extractId(op)
            reservedIds = ["CSH", "this"]
            if op[0] not in reservedIds:
                if idHold[1] == "":
                    idHold[0] = op[0]
                    self.performSelectedOperation(idHold[0], op[1], op[3], None, op[2])
                else:
                    self.performSelectedOperation(idHold[0], op[1], op[3], idHold[1], op[2])

                if "evLog" in self.objList[self.resolveIdToIndex(idHold[0])].tag.keys():
                    self.objList[self.resolveIdToIndex(idHold[0])].tag["evLog"].append(op[1])
                else:
                    self.objList[self.resolveIdToIndex(idHold[0])].tag.update({"evLog": [op[1]]})

            else:
                if idHold[1] == "":
                    idHold[0] = op[0]
                    self.performSelectedOperation(idHold[0], op[1], op[3], None, op[2])
                else:
                    self.performSelectedOperation(idHold[0], op[1], op[3], idHold[1], op[2])

        self.moveThreadAlong()
        return "Shift Complete"

    # use .start() NOT .run()
    def run(self):
        """obligatory Thread.run
    runs update dependant on self.runBehavior"""
        # continued
        if self.runBehavior[0] == 'c':
            while self.update(self.runBehavior[1]) != "No operations":
                continue
                # put this line back if you want to be annoyed
                # print("1No operations left to preform\n stopping!")
        # goal
        elif self.runBehavior[0] == 'g':
            self.updateWithGoal(self.runBehavior[2], self.runBehavior[3], self.runBehavior[4], self.runBehavior[1],
                                self.runBehavior[5])
        # iterations
        elif self.runBehavior[0] == 'i':
            while self.runBehavior[2] > 0:
                self.update(self.runBehavior[1])
                self.runBehavior[2] -= 1
        else:
            return "specify a mode"

    def updateWithGoal(self, objId, comparator, goal, subObjReference=None, saveToScene=False):
        """update but check if a value at an sysObject in self.objectList is equal, more than, less than, etc... of a goal
        value. When that goal is met stop updating."""
        if comparator == '==':
            if subObjReference is None:
                while goal != self.resolveIdToIndex(objId):
                    # stop updating if the goal is what you want it to be
                    self.update(saveToScene)
            else:
                while goal != self.unpackSubObjFromExtension(self.resolveIdToIndex(objId), subObjReference):
                    self.update(saveToScene)
        elif comparator == '!=':
            if subObjReference is None:
                while goal == self.resolveIdToIndex(objId):
                    self.update(saveToScene)
            else:
                while goal == self.unpackSubObjFromExtension(self.resolveIdToIndex(objId), subObjReference):
                    self.update(saveToScene)
        elif comparator == '>':
            if subObjReference is None:
                while goal <= self.resolveIdToIndex(objId):
                    self.update(saveToScene)
            else:
                while goal <= self.unpackSubObjFromExtension(self.resolveIdToIndex(objId), subObjReference):
                    self.update(saveToScene)
        elif comparator == '<':
            if subObjReference is None:
                while goal >= self.resolveIdToIndex(objId):
                    self.update(saveToScene)
            else:
                while goal >= self.unpackSubObjFromExtension(self.resolveIdToIndex(objId), subObjReference):
                    self.update(saveToScene)
        elif comparator == '>=':
            if subObjReference is None:
                while goal < self.resolveIdToIndex(objId):
                    self.update(saveToScene)
            else:
                while goal < self.unpackSubObjFromExtension(self.resolveIdToIndex(objId), subObjReference):
                    self.update(saveToScene)
        elif comparator == '<=':
            if subObjReference is None:
                while goal > self.resolveIdToIndex(objId):
                    self.update(saveToScene)
            else:
                while goal > self.unpackSubObjFromExtension(self.resolveIdToIndex(objId), subObjReference):
                    self.update(saveToScene)
        else:
            print("the comparator inputted is not valid")

    def replayScene(self, scn, lastShift=None):
        """use a scene's script rather than an sysObject's tasker to update the sysObject
        acts to playback a scene
        may return a string if something goes wrong"""
        self.objList = scn.obj
        if lastShift is None:
            script = scn.scp[1:]
        else:
            script = scn.scp[1:lastShift]
        for shift in script:
            if not self.objList:
                return "No objects to process"
            self.areOperationsPossible(shift)
            for operation in shift:
                idHold = self.extractId(operation)
                if idHold[1] == "":
                    idHold[0] = operation[0]
                    self.performSelectedOperation(self.resolveIdToIndex(idHold[0]), operation[1], operation[3], None,
                                                  operation[2])
                else:
                    self.performSelectedOperation(self.resolveIdToIndex(idHold[0]), operation[1], operation[3],
                                                  idHold[1],
                                                  operation[2])
        scn.obj = self.objList
        self.objList = []
        return scn.obj


class operationNotPossible(Exception):
    """exception to handle operations where the method listed is invalid for the target sysObject"""

    def __init__(self, expression, message="one or more operations are not available as writen"):
        self.expression = expression
        self.message = message


class objectNotInObjList(Exception):
    """exception to handle targets in operations that don't refer to an sysObject in CGESession.objList"""

    def __init__(self, objId):
        self.objId = objId
        self.message = "the sysObject:" + str(self.objId) + "is not in the objList"


class objectDoesNotContainTsk(Warning):
    """warning for if an sysObject does not have a thread or a tasker
    its a warning as the session will just skip over the sysObject"""
    pass
