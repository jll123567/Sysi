#import
import thread.ram

#setup
#host-usr
#else-list of obj specified type only

def setup(host,uni,cont,usr,wep,dev,obj,dta):
    thread.ram.store(host)
    for i in host.trd["ram"]:
        thread.ram.free(host,None)
    thread.ram.load(host,uni)
    thread.ram.load(host,usr)
    thread.ram.load(host,wep)
    thread.ram.load(host,dev)
    thread.ram.load(host,obj)
    thread.ram.load(host,dta)
    thread.ram.load(host,host)

def simulated(host):
    sim=True
    while sim:
        prof=[]
        for i in host.trd["ram"][0]:
            for f in i.rule:
                prof.append(f)
        #for i in host.trd["ram"][1]:
            
#runtime
if __name__ == "__main__":
    print("v10.0")