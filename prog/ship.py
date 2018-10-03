# a really simple way to label relationships
# module type: prog
# This is ridiculously stupid so don't use it seriously
#   ship db
#   [[u0,u1,type],ship,ship]
#       4 true love/Nemesis
#       3 s##ual love/NOP
#       2 crush/rival
#       1 friend/dbag
#       0 neutral
#       neg is - pos is +


# adds a ship
# u0(usr)*, u1(usr)*, shipType(int)*, db(dta)*
# updated db(dta)
def ship(u0, u1, shipType, db):
    db.storage.append([u0, u1, shipType])
    return db


# removes a ship from the db
# db(dta)*, index(int)*
# updated db(dta)
def sinkShip(db, index):
    db.storage.pop(index)
    return db


# display the data in the db
# db(dta)*
# Console Output(str)
def dispDb(db):
    for i in db.storage:
        print(i[0], ",", i[1], ",", i[2], ",")


# Info at run
if __name__ == "__main__":
    print("a really simple way to label relationships\nmodule type: prog")
