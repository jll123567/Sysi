#import

#code
#trnsf
    #interface=[data sent,data receved]
def send(obj0,obj1,dta):
    pkg=dta
    pkg.tag["sender"]=obj1.tag["name"]
    obj1.trd["trnsf"][1]=pkg
    obj0.trd["trnsf"][0]=pkg
    
def receve(obj):
    load(obj,obj.trd["trnsf"][1])

    
    #runtime
if __name__ == "__main__":
    print("basic transfer protocol v10.0")
#notes

#auth
"""by jacob ledbetter"""