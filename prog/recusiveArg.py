#import

#setup
def p0(a,r):
    if r==None:
        print("end")
    else:
        print(r)
        a+=1
        p1(a,"arg")
def p1(a,r):
    if r==None:
        print("end")
    else:
        a+=1
        p0(a,"arg")

#runtime
if __name__ == "__main__":
    print("recursive argument simulation v11.0")
    p0(0,"init")