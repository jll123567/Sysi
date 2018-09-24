# setup


class cpx:
    def __init__(self, problems=None, solutions=None):
        if problems is None:
            self.problems = []
        else:
            self.problems = problems
        if solutions is None:
            self.solutions = []
        else:
            self.solutions = solutions

    # makes a new unsolved problem labled <problem> at <obj>.trd["cpx"] with the default solution None
    # Use: <obj> = Sysh.threadModules.complex.newProblem(<obj>, <string or dta>)
    # Requires: obj with cpx core @ trd
    def newProblem(self, problem):
        self.problems.append(problem)
        self.solutions.append(None)

    # post the solution of a problem
    # Use: <obj> = Sysh.threadModules.complex.postSolution(<obj>, <string or dta>, <index of problem>
    #                                                                        or <obj>.trd["cpx"].index(<problem>)
    # Requires:obj with cpx core @ trd
    def postSolution(self, solution, problemIndex):
        self.solutions.insert(problemIndex, solution)


# runtime
if __name__ == "__main__":
    print("complex logic v11.0")
