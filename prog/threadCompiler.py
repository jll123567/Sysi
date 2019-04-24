import re
from thread_modules.tasker import tsk


# OPERATION{
#     Target, Method, Prams, Source
# }
# SHIFT{OPERATION{}, ...}
# PROFILE{SHIFT{}, ...}
# CURRENT{SHIFT{}}
#
# whitespace is not parsed accept for in Prams.
# Keywords have open and close brackets.
# Lists of elements are comma delimited.
# OPERATION
#     Keyword for an operation, requires four elements  comma separated.
#     Target: the target for the operation, converted to a string when compiled(ex. a -> "a")
#     Method: the method the target will execute, converted to a string when compiled(ex. a -> "a")
#     Prams: Parameters for the operation, copied uncommitted
#         Prams must be a python list.(ex. [a, b, c, d])
#         for methods with no parameters supply an empty list(ex. [])
#     Source: the object that made the request, converted to a string when compiled(ex. a -> "a")
#
# SHIFT
#     Keyword for a shift.
#     Only accepts OPERATIONs.
#     OPERATIONs must be comma delimited
#
# PROFILE
#     Keyword for a thread_modules.tsk profile.
#     Only one PROFILE may exist in a file
#     Only accepts SHIFTs, comma delimited.
#     If PROFILE in in the file, compiler will output a thread_modules.tsk.
#
# CURRENT
#     Keyword for a thread_modules.tsk current.
#     Only one CURRENT may exist in a file
#     Only accepts a single SHIFT.
#     If CURRENT in in the file, compiler will output a thread_modules.tsk.
#
# basic example
#
# CURRENT{
#     SHIFT{
#         OPERATION{
#             a,
#             print,
#             ["Hello, World!"],
#             a,
#         }
#     }
# }
#
# compact
# CURRENT{SHIFT{OPERATION{a,print,["Hello, World!"],a,}}}
#
# Steps
#     read file
#     remove whitespace
#     parse for profile / current
#         prep read
#         recurse shifts
#         output tsk
#     parse shift
#         recurse operations
#         output shift
#     parse operations
#         output operation
#
# script from shell???

# todo: trash this, use regular expressions

def removeWhitespace(fileContents):
    """Remove all whitespace characters from <fileContents> unless its in brackets; returns the formatted text."""
    bracketSearch = False
    formattedContent = ""
    for char in fileContents:
        if bracketSearch:
            if char == "]":
                formattedContent += char
                bracketSearch = False
            else:
                formattedContent += char
        elif re.match(r"\s", char):
            continue
        elif char == "[":
            formattedContent += char
            bracketSearch = True
        else:
            formattedContent += char
    return formattedContent


def formatOperation(text):
    """Format <text> to be a valid operation."""
    operation = re.search(r"OPERATION{(.*),(.*),(\[.*\]),(.*)}", text)
    return '["' + operation.group(1) + '","' + operation.group(2) + '",' + operation.group(3) + ',"' + operation.group(
        4) + '"]'


def formatShift(text):
    """Format the SHIFT in <text> and return it."""
    shift = re.findall(r"OPERATION{.*},|OPERATION{.*}}", text)
    outputText = "["
    for operation in shift:
        print(operation[:-1])
        try:
            outputText += (str(formatOperation(operation[:-1])) + ',')
        except TypeError:
            raise ThreadCodeWarning(text, "No operations passed.")
    if outputText[-1] == ',':
        outputText = outputText[:-1]
    outputText += ']'
    return outputText


def formatProfile(text):
    """Format the PROFILE in <text> and return it."""
    profile = re.findall(r"SHIFT{.*}},|SHIFT{.*}}}", text)
    outputText = "["
    for shift in profile:
        print(shift[:-1])
        try:
            outputText += (str(formatShift(shift[:-1])) + ',')
        except TypeError:
            raise ThreadCodeWarning(text, "No shifts passed.")
    if outputText[-1] == ',':
        outputText = outputText[:-1]
    outputText += ']'
    return outputText


def formatCurrent(text):
    """Format the PROFILE in <text> and return it."""
    # todo: error if more than one shift
    current = re.findall(r"SHIFT{.*}}}", text)
    outputText = "["
    for shift in current:
        print(shift[:-1])
        try:
            outputText += (str(formatShift(shift[:-1])) + ',')
        except TypeError:
            raise ThreadCodeWarning(text, "No shifts passed.")
    if outputText[-1] == ',':
        outputText = outputText[:-1]
    outputText += ']'
    return outputText


def parseFile(file):
    """take a file and parse it for thread code, returning any found"""
    fileData = open(file, 'r').read()
    fileData = removeWhitespace(fileData)
    outputTrd = None
    outputText = None
    profileSet = False
    currentSet = False
    if "PROFILE" in fileData or "CURRENT" in fileData:
        outputTrd = tsk()
        bracketCount = 0
        for shifter in range(0, fileData.__len__() - 1):
            if fileData[shifter] == '[':
                bracketCount += 1
            elif fileData[shifter] == ']':
                bracketCount -= 1
            if bracketCount < 0:
                raise ThreadCodeSyntaxError(fileData, "Too many closing brackets.")
            if bracketCount == 0:
                if fileData[shifter: shifter + 8] == "CURRENT{" and not currentSet:
                    currentSet = True
                    braceCount = 1
                    subBracketCount = 0
                    temp = "CURRENT{"
                    for subShift in range(shifter + 8, fileData.__len__()):
                        if fileData[subShift] == '[':
                            subBracketCount += 1
                        elif fileData[subShift] == ']':
                            subBracketCount -= 1
                        if subBracketCount < 0:
                            raise ThreadCodeSyntaxError(fileData, "Too many closing brackets.")
                        if subBracketCount == 0:
                            if fileData[subShift] == '{':
                                braceCount += 1
                            elif fileData[subShift] == '}':
                                braceCount -= 1
                            if braceCount < 0:
                                raise ThreadCodeSyntaxError(fileData, "Too many closing braces.")
                        temp += fileData[subShift]
                        if braceCount == 0:
                            temp += '}'
                            outputTrd.current = formatTskAtribs(temp)
                if fileData[shifter: shifter + 8] == "PROFILE{" and not profileSet:
                    profileSet = True
                    braceCount = 1
                    subBracketCount = 0
                    temp = "PROFILE{"
                    for subShift in range(shifter + 8, fileData.__len__()):
                        if fileData[subShift] == '[':
                            subBracketCount += 1
                        elif fileData[subShift] == ']':
                            subBracketCount -= 1
                        if subBracketCount < 0:
                            raise ThreadCodeSyntaxError(fileData, "Too many closing brackets.")
                        if subBracketCount == 0:
                            if fileData[subShift] == '{':
                                braceCount += 1
                            elif fileData[subShift] == '}':
                                braceCount -= 1
                            if braceCount < 0:
                                raise ThreadCodeSyntaxError(fileData, "Too many closing braces.")
                        temp += fileData[subShift]
                        if braceCount == 0:
                            outputTrd.profile = formatTskAtribs(temp)
    else:
        outputText = formatTskAtribs("PROFILE{" + fileData + "}")
    if outputTrd is not None:
        return outputTrd
    elif outputText is not None:
        return outputText
    else:
        raise UnknownError()


class ThreadCodeSyntaxError(Exception):
    def __init__(self, expression, badSyntaxType):
        self.message = "The following is incorrect syntax: " + str(badSyntaxType)
        self.expression = expression


class ThreadCodeWarning(Warning):
    def __init__(self, expression, message):
        self.message = message
        self.expression = expression


class UnknownError(Exception):
    def __init__(self):
        self.message = "Something went horribly wrong in the thread compiler!"
