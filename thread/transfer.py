# import
from . import ram


# setup
# trnsf
# interface=data receved
# note: sent data must have a "sander" tag in dta.tag

def send(obj0, obj1, dta):
    pkg = dta
    pkg.tag["sender"] = obj1.tag["name"]
    obj0.trd["trnsf"] = pkg
    return obj0


def receive(obj):
    obj = ram.load(obj, obj.trd["trnsf"])
    return obj


# runtime
if __name__ == "__main__":
    print("basic transfer protocol v10.0")
