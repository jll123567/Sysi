# really basic area for problem solving
# module type: def
# [problem0, problem1], [solutions for 0,solutions for 1]
import sys_objects


# complex Thread module
# problems[], solutions[]
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

    # makes a new unsolved problem labeled <problem> at <obj>.trd["cpx"] with the default solution None
    # problem(any)*
    # none
    def newProblem(self, problem):
        self.problems.append(problem)
        self.solutions.append(None)

    # post the solution of a problem
    # solution(any)*, problemIndex(int)
    # none
    def postSolution(self, solution, problemIndex=0):
        self.solutions.insert(problemIndex, solution)

    # pack data for ram
    # none
    # dta(cpx attribs, tags)
    def package(self):
        return sys_objects.data([self.problems, self.solutions], {"name": "tread.cpx.package", "id": None,
                                                             "dataType": "thread.cpx.package"})


# Info at run
if __name__ == "__main__":
    print("really basic area for problem solving\nmodule type: def\n[problem0, problem1], [solutions for 0,"
          "solutions for 1]")
