#import
import re,thread.ram

#setup
#mem[internal,real,storage]
#[obj,obj,...]stored in order of date added            
def load(usr,dir,index):
    if dir==0:
        print("no internal access")
    else:
        thread.ram.load(usr,usr.mem[dir][index])
        
def forget(user,dir,index):
    if dir==0:
        print("no internal access")
    else:
        user.mem[dir].pop(index)
            
def store(user,dir,object):
    if dir==0:
        print("no internal access")
    else:
        user.mem[dir].append(object)
            
def find(user,query):
    if query == None:
        query=input()
    for d in range(1,2):
        for i in user.mem[d]:
            for t in i.tag:
                if re.match(str(t),r"*(.)"+query+r"*(.)"):
                    print(t)
                else:
                    print(None)
                        
def modify(user,dir,index,value):
    if dir == 0:
        print("no internal access")
    else:
        user.mem[dir][index]=value

#runtime
if __name__ == "__main__":
    print("user memory v10.0")