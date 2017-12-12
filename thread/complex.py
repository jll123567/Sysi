#import
import math
#code
#complex
#[[p0,p1],result]    
def newProblem(obj,problem):
        obj.trd["cpx"][0].append(problem)

def post(obj,solution):
    obj.trd["cpx"][1]=solution
        
def solve(obj):
    for i in obj.trd["cpx"][0]:
        post(obj,i)
    
    #runtime
if __name__ == "__main__":
    print("complex logic v10.0")
#notes

#auth
"""by jacob ledbetter"""