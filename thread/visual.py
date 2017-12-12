#import

#code
#visual
#feed=[raw,pitch,yaw,roll,[obj]]
def capture(usr):
    usr.mem[1].append(usr.trd["vis"][0])
"""def id(obj):
    print("working on it")
    feed[3].append(object(get(model),get(trd),get(tags)))"""
def target(obj,p,y,r):
    obj.trd["vis"][1]=p
    obj.trd["vis"][2]=y
    obj.trd["vis"][3]=r
    
    #runtime

#notes

#auth
"""by jacob ledbetter"""