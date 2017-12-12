#import

#code
#move
#    [x pos,y pos,z pos,x accel,y accel, z accel, new x,new y,new z] 
def warp(obj,x,y,z):
    obj.trd["mov"][0]=x
    obj.trd["mov"][1]=y
    obj.trd["mov"][2]=z

def move(obj):
    obj.trd["mov"][0]+=obj.trd["mov"][3]
    obj.trd["mov"][1]+=obj.trd["mov"][4]
    obj.trd["mov"][2]+=obj.trd["mov"][5]

def moveTo(obj,x,y,z):
    while obj.trd["mov"][0]!=x and obj.trd["mov"][1]!=y and obj.trd["mov"][2]!=z:
        if obj.trd["mov"][0]<x:
            obj.trd["mov"][0]+=obj.trd["mov"][3]
        elif obj.trd["mov"][0]>x:
            obj.trd["mov"][0]-=obj.trd["mov"][3]
        else:
            obj.trd["mov"][0]=obj.trd["mov"][0]
        if obj.trd["mov"][1]<y:
            obj.trd["mov"][1]+=obj.trd["mov"][4]
        elif obj.trd["mov"][1]>y:
            obj.trd["mov"][1]-=obj.trd["mov"][4]
        else:
            obj.trd["mov"][1]=obj.trd["mov"][1]
        if obj.trd["mov"][2]<z:
            obj.trd["mov"][2]+=obj.trd["mov"][5]
        elif obj.trd["mov"][2]>z:
            obj.trd["mov"][2]-=obj.trd["mov"][5]
        else:
            obj.trd["mov"][2]=obj.trd["mov"][2]
    
    #runtime
if __name__ == "__main__":
    print("move thread bolck v10.0")
#notes

#auth
"""by jacob ledbetter"""