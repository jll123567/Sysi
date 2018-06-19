# setup
# visual
# feed=[raw,pitch,yaw,roll,[obj]]


# set camera rotation
# use: <obj> = rotate(<obj>, <int representing pitch>, <int representing yaw>, <int representing roll>)
# requires: obj
def rotate(obj, p, y, r):
    obj.trd["vis"][1] = p
    obj.trd["vis"][2] = y
    obj.trd["vis"][3] = r
    return obj


# runtime
if __name__ == "__main__":
    print("visuals v11.0")
