# import
from math import sqrt


# setup
# [time passed(in hours),refrence count,importance(0,100)]
# (100*0.33^hours) + (sqrt(refrences)*10) + (isCurrent()*25) + importance(0,100)
def calculate_relevancy(obj):
    if obj.tag["relevancy"][1] == 0:
        return 100 + (sqrt(obj.tag["relevancy"][1]) * 10) + 25 + (obj.tag["relevancy"][2])
    else:
        return (100 * ((1 / 3) ** obj.tag["relevancy"][0])) + (sqrt(obj.tag["relevancy"][1]) * 10) + (obj.tag["relevancy"][2])


# runtime
if __name__ == "__main__":
    print("relevancy calc v11.0")
