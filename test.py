"""don't mind me, just being dumb"""

import thread_modules.state_of_mind as state_of_mind
import attribs.personality as personality

b = personality.prs(["reverted"], None, None)
a = state_of_mind.SOMObject()
a.trd.somm = state_of_mind.SOMManger(None, None, None, b)
a.prs.goals.append("save me!")
print(a.prs.goals)
a.revertSOMStateToPrevious()
a.revertSOMStateToDefault()
print(a.prs.goals)

# test two remaingin user functions

