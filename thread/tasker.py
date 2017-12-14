#import
import time
#setup
    #tasker
    #tsk=[profile,profile,profile,...]
        #profile=[f0,f1,f2,...]
    #first profile is current profile

def step(usr):
    print(usr.trd["tsk"][0][0])
    usr.trd["tsk"][0].pop(0)
    if usr.trd["tsk"][0]==[]:
        usr.trd["tsk"].pop(0)

def run(usr):
    for i in usr.trd["tsk"][0]:
        print(i)
    usr.trd["tsk"].pop(0)
    
        
def react(var,val,usr,index):
    if var==val:
        newMain=usr.trd["tsk"][index]
        usr.trd["tsk"].pop(index)
        usr.trd["tsk"].insert(index,newMain)
        run(usr)

def await(var,val,usr,awaitProf):
    waiting=True
    count=0
    while waiting:
        if var==val:
            waiting=False
            run(usr)            
        else:
            usr.trd["tsk"].insert(0,awaitProf)
            step(usr)
            
def wait(t,usr):
    time.sleep(t)
    run(usr)

    
#runtime
if __name__ == "__main__":
    print("tasker v10.0")