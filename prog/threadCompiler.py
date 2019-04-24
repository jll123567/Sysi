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
#     Must be after CURRENT.
#
# CURRENT
#     Keyword for a thread_modules.tsk current.
#     Only one CURRENT may exist in a file
#     Only accepts a single SHIFT.
#     If CURRENT in in the file, compiler will output a thread_modules.tsk.
#     Must be before PROFILE.
#
# basic example
#
# CURRENT{
#     SHIFT{
#         OPERATION{a,print,["Hello, World!"],a,}
#     }
# }
#
# PROFILE{
#     SHIFT{
#         OPERATION{a,print,["Hello, World!"],a,}
#         }
#     }
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
        try:
            outputText += (str(formatShift(shift[:-1])) + ',')
        except TypeError:
            raise ThreadCodeWarning(text, "No shifts passed.")
    if outputText[-1] == ',':
        outputText = outputText[:-1]
    outputText += ']'
    return outputText


def parseFile(file):
    """take a file and parse it for thread code
    return a threadModules tasker if PROFILE or CURRENT are in the file
    return a string with either the first SHIFT or if none are found the first OPERATION
    raise an error if nothing is found
    """
    fileData = open(file, 'r').read()
    fileData = removeWhitespace(fileData)
    outputTrd = tsk()
    prf = re.search(r"(PROFILE{.*}}})", fileData)
    cur = re.search(r"(CURRENT{.*}}})P", fileData)
    shf = re.search(r"(SHIFT{.*}})", fileData)
    opr = re.search(r"(OPERATION{.*})", fileData)
    if prf or cur:
        if re.match(r".*PROFILE{.*}.*CURRENT{.*}.*}", fileData):
            raise ThreadCodeSyntaxError("PROFILE found before CURRENT.")
        if prf:
            outputTrd.profile = formatProfile(prf.group(1))
        if cur:
            outputTrd.current = formatCurrent(cur.group(1))
        return outputTrd
    elif shf:
        return formatShift(shf.group(1))
    elif opr:
        return formatOperation(opr.group(1))
    else:
        raise ThreadCodeSyntaxError("No valid keywords used or empty file.")


class ThreadCodeSyntaxError(Exception):
    def __init__(self, message, expression=None):
        self.message = "The following is incorrect syntax: " + str(message)
        self.expression = expression


class ThreadCodeWarning(Warning):
    def __init__(self, message, expression):
        self.message = message
        self.expression = expression


class UnknownError(Exception):
    def __init__(self):
        self.message = "Something went horribly wrong in the thread compiler!"
