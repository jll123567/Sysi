#import
    #import random_access_memory
import math
listing=False
out=[]
#code
#lang
#feed=[in,out]
#in=[[vol,vol,vol],[Right version of sound]] each index is one mS
#out=[vol,vol,vol](mono output)
def listen(obj,inputSource):
        global listing
        listing=True
        while listing:
            obj.trd["lang"][0].append(inputSource)
    
def store(obj):
        dta=data(obj.trd["lang"][0],{})
        obj.trd["ram"].append(dta)
        
def tune(obj,minVolume,minPan,maxPan):
    for i in obj.trd["lang"][0][0]:
        if abs(i) < minVolume:
            obj.trd["lang"][0][0][index(i)]=0
        elif minPan > 0:
            obj.trd["lang"][0][0][index(i)]=0
        elif abs(i) > minPan*(-2.2):
            obj.trd["lang"][0][0][index(i)]
        else:
            continue
    
    for i in obj.trd["lang"][0][1]:
        if abs(i) < minVolume:
            obj.trd["lang"][0][1][index(i)]=0
        elif maxPan < 0:
            obj.trd["lang"][0][0][index(i)]
        elif abs(i) < maxPan*2.2:
            obj.trd["lang"][0][0][index(i)]
        else:
            continue
def silence(obj):
    obj.trd["lang"][1]=[]
#sounds mono[vol0,vol1,vol2]    
def queueSpeak(obj,sounds):
    obj.trd["lang"][1]=sounds
    
def speak(obj):
    global out
    for i in obj.trd["lang"][1]:
        out.append(i)
    obj.trd["lang"][1]=[]

    
    #runtime
if __name__ == "__main__":
    print("language management v10.0")
#notes

#auth
"""by jacob ledbetter"""