#import

#code
    #def
#[[master line end point],[id,parent id,start offset,endpoint],...]
def fork(uni,lineId,parent,offset,endpoint):
    count=0
    invalid=True
    for i in uni.tl:
        if count==0:
            if lineId==0:
                print("invalid id")
                invalid=True
            else:
                invalid=False
                count+=1
        else:
            if i[0]==lineId:
                print("id already in use")
                invalid=True
                count+=1
            else:
                count+=1
    if not invalid:
        uni.tl.append([lineId,parent,offset,endpoint])

def prune(uni,id):
    for i in uni.tl:
        if i[0]==id:
            uni.tl.pop(i.index())
    for i in uni.scn:
        if i.scp[0][1]==id:
            unplot(i)

def plot(uni,scn,lineId,t):
    inUni=False
    for i in uni.tl:
        if i[0]==lineId:
            if i[3]<t:
                extend(uni,lineId,t-i[3])
            inUni=True
    if not inUni:
        print(lineId," is not a valid line in ",uni.tag["name"])
    else:
        if scn.scp[0]!=["-","-"]:
            scn.scp.insert(0,[t,lineId])
        else:
            scn.scp[0]=[t,lineId]

def unplot(scn):
    scn.scp[0]=["-","-"]
            
def extend(uni,lineId,timeToAdd):
    for i in uni.tl:
        if i[0]==lineId:
            i[3]+=timeToAdd

def getTotalOffset(uni,id,off):
    for i in uni.tl:
        if i[0]==id:
            off+=i[3]
            if i[1]==0:
                return off
            else:
                getTotalOffset(uni,i[1],off)

#timePerSymb is either "h","d"
def view(uni,timePerSymb):
    def acuratePlot(uni,branchId,timePerSymb):
        offset=0
        text="."
        for i in uni.scn:
            if i.scp[0]==branchId:
                new=(("-"*((i.scp[0]-offset)/timePerSymb))+"|")
                text+=new
                offset=i.scp[0]
            if uni.scn[uni.scn.index(i)+1].scp[1]!=branchId:
                text+="."
        return text
        
    if timePerSymb=="h":
        timePerSymb=60*60
    elif timePerSymb=="d":
        timePerSymb=60*60*24
    else:
        timePerSymb=timePerSymb
        
    for i in uni.tl:
        if i.len()==1:
            print(acuratePlot(uni,0,timePerSymb))
        else:
            print((" "*(getTotalOffset(uni,i[1],0)))+(acuratePlot(uni,i[0],timePerSymb)))
            
    #runtime
if __name__ == "__main__":
    print("timeline management v10.0")
#notes

#auth
"""by jacob ledbetter"""