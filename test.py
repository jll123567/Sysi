import object
f = object.user()
print(f.tag)
g = object.user(f.mod, f.trd, f.prs, f.mem, {"name": "hello"})
print(g.tag)
h = object.user()
print(h.tag, "\n\n")
print(g.tag)
g.tag["name"] = "goodbye"
print(g.tag)
