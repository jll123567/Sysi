# setup
# transf
# interface = container for receved data


# sends <data> form an object to another
# use <obj> = Sysh.thread.transfer.send(<obj>, <sender>, <dta>
# requres: 2 obj (sender and obj) and dta
def send(obj, sender, dta):
    pkg = dta
    pkg.tag.update({"sender": sender.tag["name"]})
    obj.trd["transf"] = pkg
    return obj


# runtime
if __name__ == "__main__":
    print("basic transfer protocol v10.0")
