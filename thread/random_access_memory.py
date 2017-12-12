#import
import re
    #import obj
#code
#random access memory        
#[...,...]
def load(obj,dta):
    obj.trd["ram"].append(dta)
    
def read(obj):
    for i in obj.trd["ram"]:
        print(i)
def search(obj,query):
    for i in obj.trd["ram"]:
        if re.match(str(i),(r"*(.)"+query+r"*(.)")):
            print(i)
            print(index(i))
            matched=True
    if matched != True:
        print("no results. try random_access_memory.read(obj)")
    
def store(usr):
    dta=data([usr.trd["ram"]],{})
    usr.mem[1].append(dta)
    
def free(obj,index):
    if index == None:
        obj.trd["ram"].pop(-1)
    else:
        obj.trd["ram"].pop(index)
    
    #runtime
if __name__ == "__main__":
    print("random access memory manager v10.0")
#notes

#auth
"""by jacob ledbetter"""