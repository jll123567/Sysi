#import
#import obj
#code
#queue
#format[task one,two,[sub one,sub two]]
# instruction="i/e : task"
# e is for exact code like tasks and i is for inexact string or english like tasks
def load(obj,memeory):
    obj.trd["que"]=obj.mem[0][memory].d
    
def close(obj):
        obj.trd["que"]=[]
    
def save(obj,tags):
    lastQueue=data(obj.trd["que"],tags)
    obj.mem[0].append(lastQueue)
    print("queue saved to: ",lastQueue,"@",obj.tag["name"],".mem")
    
def add(obj,task):
    obj.trd["que"].append(task)
    
def interupt(que,task,index):
    obj.trd["que"].insert(index,task)
        
def complete(obj,i):
        if i==None:
            obj.trd["que"].pop(0)
        else:
            obj.trd["que"].pop(i)
        
def run(obj,indent):
    for i in obj.trd["que"]:
        if i == type([1,2]):
            run(i,indent+1)
        else:
            if i[0]=="e":
                print("  "*indent,"exact:",i)
            elif i[0]=="i":
                print("  "*indent,"inexact:",i)
            else:
                print("Not a valid task type")

    
    #runtime
if __name__ == "__main__":
    print("queue v10.0")
#notes

#auth
"""by jacob ledbetter"""