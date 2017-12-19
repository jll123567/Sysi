# setup
def saveUni(uni, fileName):
    file = open(fileName+".py", 'w')
    sameBegin = "# AUTO GENERATED CODE\nimport object\ndef load():\n    uni=object.universe("
    variableMiddle = str(uni.tl)+","+str(uni.scn)+","+str(uni.obj)+","+str(uni.cont)+","+str(uni.funct)+","+str(uni.rule)+","+str(uni.tag)
    sameEnd = ")\n    return uni\n# END AUTO GENERATED CODE\n# TO USE: IMPORT THIS FILE AND RUN " + fileName + ".load()"
    file.write(sameBegin + variableMiddle + sameEnd)


def saveScn(scn, fileName):
    file = open(fileName+".py", 'w')
    sameBegin = "# AUTO GENERATED CODE\nimport object\ndef load():\n    uni=object.universe("
    variableMiddle = str(scn.scp) + "," + str(scn.obj) + "," + str(scn.loc) + "," + str(scn.tag)
    sameEnd = ")\n    return uni\n# END AUTO GENERATED CODE\n# TO USE IMPORT THIS FILE AND RUN " + fileName + ".load()"
    file.write(sameBegin + variableMiddle + sameEnd)


# runtime
if __name__ == "__main__":
    print("Save uni v10.0")
