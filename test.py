"""don't mind me, just being dumb"""

import thread_modules.state_of_mind as state_of_mind
import attribs.personality as personality

a = state_of_mind.SOMObject()
a.trd.somm = state_of_mind.SOMManger()
b = personality.prs(["success"], [], [])
a.trd.somm.addState(state_of_mind.state("test", b))
print(a.prs.goals)
a.changeSOMState("test", False)
print(a.prs.goals)
