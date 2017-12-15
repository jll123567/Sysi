#import
import object,thread.ram,thread.tasker

#setup
#host-usr
#else-list of obj specified type only

def setup(host,uni,cont,usr,wep,dev,obj,dta,hostInternal):
    sysh.thread.random_access_memory.store(host)
    for i in host.trd["ram"]:
        thread.ram.free(host,None)
    thread.ram.load(host,dta)
    thread.ram.load(host,uni)
    thread.ram.load(host,usr)
    thread.ram.load(host,wep)
    thread.ram.load(host,dev)
    thread.ram.load(host,obj)
    thread.ram.load(host,hostInternal)

def simulated(host):
    sim=True
    while sim:
        prof=[]
        for i in host.trd["ram"][1]:
            for f in i.rule:
                prof.append(f)
        host.trd["tsk"].insert(0,prof)
        thread.tasker.run(host)
        prof=[]
        for i in host.trd["ram"][2]:
            host.trd["tsk"].insert(0,i.trd["tsk"][0])
            i.trd["tsk"].pop(0)
            tread.tasker.run(host,i.trd["tsk"])
        for i in host.trd["ram"][3]:
            host.trd["tsk"].insert(0,i.trd["tsk"][0])
            i.trd["tsk"].pop(0)
            tread.tasker.run(host,i.trd["tsk"])
        for i in host.trd["ram"][4]:
            host.trd["tsk"].insert(0,i.trd["tsk"][0])
            i.trd["tsk"].pop(0)
            tread.tasker.run(host,i.trd["tsk"])
        for i in host.trd["ram"][5]:
            host.trd["tsk"].insert(0,i.trd["tsk"][0])
            i.trd["tsk"].pop(0)
            tread.tasker.run(host,i.trd["tsk"])
        for i in host.trd["ram"][6]:
            host.trd["tsk"].insert(0,i.trd["tsk"][0])
            i.trd["tsk"].pop(0)
            tread.tasker.run(host,i.trd["tsk"])
        
#runtime
if __name__ == "__main__":
    print(" simulated real "imm" v10.0")
