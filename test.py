"""don't mind me, just being dumb"""
a = {}
try:
    try:
        try:
            print(a["a"])
        except ArithmeticError:
            pass
    except KeyError:
        print("caught!")
except KeyError:
    print("caught!1")
