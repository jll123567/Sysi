# Definition for damage profile
# ModType:Def

# Damage Profiles (wep.dmg)
# damages = {atrib to modify: ammouunt(int), ...}
class dmg:
    def __init__(self, damages=None):
        if damages is None:
            self.damages = {"health": 0}
        else:
            self.damages = damages


# Info at run
if __name__ == "__main__":
    print("Definition for damage profile\nModType:Def")
