"""
Take .trc files and turn them into valid operations, shifts, profiles, or currents.
To use from command-line:
    Move or copy this file to sysh root directory. (*/sysh/)
    Run with "python threadCompiler.py <filename>"
    Prints to stdout.
    Profiles and currents are followed by a newline.
To use from a python module:
    import prog.threadCompiler
    parseFile(<filename>, <formatting="-t">) returns the thread code.
"""
import re
from thread_modules import Tasker
from sys import argv
import warnings


# OPERATION{
#     Target, Method, Prams, Source
# }
# SHIFT{OPERATION{}, ...}
# PROFILE{SHIFT{}, ...}
# CURRENT{SHIFT{}}
#
# whitespace is not parsed accept for in Prams.
# Lists of elements are comma delimited.
#
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
#     Keyword for a thread_modules.Tasker profile.
#     Only one PROFILE may exist in a file
#     Only accepts SHIFTs, comma delimited.
#     If PROFILE in in the file, compiler will output a thread_modules.Tasker.
#     Must be after CURRENT.
#
# CURRENT
#     Keyword for a thread_modules.Tasker current.
#     Only one CURRENT may exist in a file
#     Only accepts a single SHIFT.
#     If CURRENT in in the file, compiler will output a thread_modules.Tasker.
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
# Output:
#


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

    # syntax check
    if re.match(r"{", operation.group(1)):
        warnings.warn("\nFound a target that looks weird.\nDid you write \"OPERATION{{\"?", StrangeObjectName)
    if re.match(r".*}", operation.group(4)):
        warnings.warn(
            "\nFound a source that looks weird.\nDid you write did you close an OPERATION with an extra \"}\"?",
            StrangeObjectName)

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
            warnings.warn(NoElementPassed)
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
            warnings.warn(NoElementPassed)
    if outputText[-1] == ',':
        outputText = outputText[:-1]
    outputText += ']'
    return outputText


def formatCurrent(text):
    """Format the PROFILE in <text> and return it."""
    current = re.findall(r"SHIFT{.*}}}", text)
    outputText = ""
    for shift in current:
        try:
            outputText += (str(formatShift(shift[:-1])) + ',')
        except TypeError:
            warnings.warn(NoElementPassed)
    if outputText[-1] == ',':
        outputText = outputText[:-1]
    return outputText


def parseFile(file, outputFormat="-t"):
    """take a file and parse it for thread code
    <outputFormat> as "-t" for text, "-o" for a tasker object(if supported).
    return a threadModules tasker if PROFILE or CURRENT are in the file
    return a string with either the first SHIFT or if none are found the first OPERATION
    raise an error if nothing is found
    """
    fileData = open(file, 'r').read()
    fileData = removeWhitespace(fileData)
    outputTrd = Tasker()
    outputTxt = ""

    # syntax check
    op = re.findall(r"{(?!(?!.*\[).*\])", fileData).__len__()
    cls = re.findall(r"}(?!(?!.*\[).*\])", fileData).__len__()
    if op != cls:
        warnings.warn(
            "\nThere may be an unmatched brace in code.\nHowever, this may false trigger for a parameter in an operation",
            UnmatchedBrace)

    if re.match(r".*\[.*[\[\]{}].*\].*", fileData):
        warnings.warn("\nCode may not be parsed correctly due to a [ ] { or } between []", SpecialCharInPram)

    prf = re.search(r"(PROFILE{.*}}})", fileData)
    cur = re.search(r"(CURRENT{.*}}})P", fileData)
    shf = re.search(r"(SHIFT{.*}})", fileData)
    opr = re.search(r"(OPERATION{.*})", fileData)
    if prf or cur:
        if re.match(r".*PROFILE{.*}.*CURRENT{.*}.*}", fileData):
            raise ThreadCodeSyntaxError("PROFILE found before CURRENT.")
        if prf:
            if outputFormat == '-o':
                outputTrd.profile = formatProfile(prf.group(1))
            elif outputFormat == '-t':
                outputTxt += (formatProfile(prf.group(1)) + "/n")

        if cur:
            if outputFormat == '-o':
                outputTrd.profile = formatProfile(cur.group(1))
            elif outputFormat == '-t':
                outputTxt += (formatProfile(cur.group(1)) + "\n")
        if outputTxt != "":
            return outputTxt
        else:
            return outputTrd
    elif shf:
        return formatShift(shf.group(1))
    elif opr:
        return formatOperation(opr.group(1))
    else:
        raise ThreadCodeSyntaxError("No valid keywords used or empty file.")


class ThreadCodeSyntaxError(Exception):
    """Raised if syntax is wrong."""

    def __init__(self, message, expression=None):
        self.message = "The following is incorrect syntax: " + str(message)
        self.expression = expression


class UnmatchedBrace(Warning):
    """Raised if there are an odd number of braces."""
    pass


class StrangeObjectName(Warning):
    """Raised if operation has leading or trailing braces."""
    pass


class NoElementPassed(Warning):
    """Raised if no elements were passed where one was expected."""
    pass


class SpecialCharInPram(Warning):
    """Raised if there is a []{ or } in prams ([])"""
    pass


class UnknownError(Exception):
    """If you see this error, run."""

    def __init__(self):
        self.message = "Something went horribly wrong in the thread compiler!"


class BadFileType(Exception):
    """Raised if the file is not of the expected type"""

    def __init__(self, expression=None):
        self.message = "threadCompiler only accepts .trc files"
        self.expression = expression


if __name__ == "__main__":
    fileName = ""
    try:
        fileName = argv[1]
    except IndexError:
        print("This script requires an argument. Use '-h' for more information")
        exit(1)
    if argv[1] == "-h":
        print("threadCompiler.py <filePath>\n\t Compiles and prints a .trc file."
              "\nthreadCompiler.py -h\n\t This help message.")
        exit(0)
    if not re.match(r".*\.trc$", fileName):
        raise BadFileType(fileName)
    else:
        outForm = "-t"
        try:
            outForm = argv[2]
        except IndexError:  # If no second argument was passed.
            pass
        print(parseFile(fileName, outForm))
