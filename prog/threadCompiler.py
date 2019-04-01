import re


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

def removeWhitespace(fileContents):
    """Remove all whitespace characters from <fileContents> unless its in brackets; returns the formatted text."""
    bracketSearch = False
    formattedContent = ""
    for char in fileContents:
        if bracketSearch:
            if re.match(r"\]", char):
                formattedContent += char
                bracketSearch = False
            else:
                formattedContent += char
        elif re.match(r"\s", char):
            continue
        elif re.match(r"\[", char):
            formattedContent += char
            bracketSearch = True
        else:
            formattedContent += char
    return formattedContent


def formatOperation(text):
    """Format <text> to be a valid operation."""
    formattedOperation = ""
    mode = "start"
    temp = ""
    bracketCount = 0
    for char in text:
        if mode == "start":
            if char == "{":
                formattedOperation += '['
                mode = "trg"
        elif mode == "trg":
            if char == ',':
                formattedOperation += ('"' + temp + "\",")
                mode = "mthd"
                temp = ""
            else:
                temp += char
        elif mode == "mthd":
            if char == ',':
                formattedOperation += ('"' + temp + "\",")
                mode = "pram"
                temp = ""
            else:
                temp += char
        elif mode == "pram":
            if bracketCount < 0:
                pass
                # raise ThreadCodeSyntaxError
            if char == '[':
                bracketCount += 1
                temp += char
            elif char == "]":
                bracketCount -= 1
                temp += char
            elif bracketCount == 0 and char == ',':
                formattedOperation += (temp + ',')
                mode = "src"
                temp = ""
            else:
                temp += char
        elif mode == "src":
            if char == '}':
                formattedOperation += ('"' + temp + "\"]")
                break
            else:
                temp += char
        else:
            pass
            # raise GenericErr
    return formattedOperation
