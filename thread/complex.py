# setup
# [[problems],[results]]


# makes a new unsolved problem labled <problem> at <obj>.trd["cpx"] with the default solution None
# Use: <obj> = Sysh.thread.complex.ne   wProblem(<obj>, <string or dta>)
# Requires: obj with cpx core @ trd
def newProblem(obj, problem):
    obj.trd["cpx"][0].append(problem)
    obj.trd["cpx"][1].append(None)
    return obj


# post the solution of a problem
# Use: <obj> = Sysh.thread.complex.postSolution(<obj>, <string or dta>, <index of problem>
#                                                                        or <obj>.trd["cpx"].index(<problem>)
# Requires:obj with cpx core @ trd
def postSolution(obj, solution, problemIndex):
    obj.trd["cpx"].insert(problemIndex, solution)
    return obj


# runtime
if __name__ == "__main__":
    print("complex logic v11.0")
