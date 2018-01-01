# setup
# [[p0,p1],result]


def newProblem(obj, problem):
    obj.trd["cpx"][0].append(problem)
    return obj


def post(obj, solution):
    obj.trd["cpx"][1] = solution
    return obj


def solve(obj):
    for i in obj.trd["cpx"][0]:
        post(obj, i)


# runtime
if __name__ == "__main__":
    print("complex logic v10.0")
