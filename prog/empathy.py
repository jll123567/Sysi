# import


# setup
def checkIteg(objPast, objCurrent):
    if objPast.tag["health"] > objCurrent.tag["health"]:
        return "reduced"
    else:
        return "maintained"


def checkWill(objPast, objCurrent):
    if objPast.tag["fucntlist"] > objCurrent.tag["functlist"]:
        return "reduced"
    else:
        return "maintained"


# runtime
if __name__ == "__main__":
    print("empathy definitions v11.0")
