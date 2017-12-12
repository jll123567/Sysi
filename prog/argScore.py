def evidence():
    working=True
    one=0
    two=0
    while working:
        f=input("1 adds to 1 2 adds to to -1 drops from 1 -2 drops from 2 done to quit \n")
        f=str(f)
        if f=="1":
            one+=1
        elif f=="2":
            two+=1
        elif f=="-1":
            one-=1
        elif f=="-2":
            two-=1
        elif f=="done":
            working=False
        else:
            print("\n invalid \n")
    if one>two:
        print("one wins")
    elif two>one:
        print("two wins")
    else:
        print("no one wins")

def opinion():
    f=input("has some one been swayed to a different view while you were left intact")
    if f=='y':
        print("swayer wins")
    else:
        print("no one wins")
    
    
        

if __name__ == "__main__":
    print("argument score v10.0")
    evidence()

# by Jacob Ledbettervf