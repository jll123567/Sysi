#ship db
    #[[u0,u1,type],ship,ship]
    #4 true love/Nemisis
    #3 s##ual love/NOP
    #2 chrush/rival
    #1 friend/dbag
    #0 nutral
    #neg is - pos is +
    
def ship(u0,u1,shipType,db):
    db.d.append([u0,u1,shipType])
    
def sinkShip(db,index):
    dd.d.pop(index)

def dispDb(db):
    for i in db.d:
        print(i[0],",",i[1],",",i[2],",")
    

if __name__ == "__main__":
    print("shipping v10.0 \n please dont use this for serious reasons...")

# by Jacob Ledbetter