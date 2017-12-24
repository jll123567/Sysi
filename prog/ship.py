# setup
#   ship db
#   [[u0,u1,type],ship,ship]
#       4 true love/Nemesis
#       3 s##ual love/NOP
#       2 crush/rival
#       1 friend/dbag
#       0 neutral
#       neg is - pos is +


def ship(u0, u1, shipType, db):
    db.d.append([u0, u1, shipType])
    return db


def sinkShip(db, index):
    db.d.pop(index)
    return db


def dispDb(db):
    for i in db.d:
        print(i[0], ",", i[1], ",", i[2], ",")


# runtime
if __name__ == "__main__":
    print("shipping v10.0 \n please do not use this for serious reasons...")
