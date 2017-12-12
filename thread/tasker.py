#import
#code
    #tasker
    #tsk=[profile,profile,profile,...]
        #profile=[f0,f1,f2,...]
def run(funct):
    print(funct)

def runProfile(prof):
    for i in prof:
        run(i)
        
def react(var,val,funct):
    if var==val:
        run(funct)

def await(var,val,funct,awaitProf):
    waiting=True
    count=0
    while waiting:
        if var==val:
            waiting=Flase
            run(funct)
        else:
            run(awaitProf[count])
            if count < len(awaitProf):
                count+=1
            else:
                count=0
def wait(t,funct):
    time.sleep(t)
    run(funct)

    
    #runtime
if __name__ == "__main__":
    print("tasker v10.0")
#notes

#auth
"""by jacob ledbetter"""