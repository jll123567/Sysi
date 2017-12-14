#import
import re
import object

#setup
#random access memory        
#[ w/e ,...]

def load(obj,dta):
    obj.trd["ram"].append(dta)
    
def read(obj):
    for i in obj.trd["ram"]:
        print(i)
def search(obj,query):
    matched=True
    for i in obj.trd["ram"]:
        if re.match(str(i),(r"*(.)"+query+r"*(.)")):
            print(i)
            print(obj.trd["ram"].index(i))
            matched=True
    if matched != True:
        print("no results. try sysh.thred.ram.read(obj)")
    
def store(usr):
    dta=object.data([usr.trd["ram"]],{})
    usr.mem[1].append(dta)
    
def free(obj,index):
    if index == None:
        obj.trd["ram"].pop(-1)
    else:
        obj.trd["ram"].pop(index)
    
#runtime
if __name__ == "__main__":
    print("random access memory manager v10.0")