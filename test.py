"""
Don't mind me, just being testing thisngs here.
Ideally this file will be removed in any sort of "real release".
"""
import sys_objects
import CGE
a = sys_objects.sysObject()
a.tag['id'] = "un/o/0"
a.blankTask()
a.trd.tsk.appendCurrent(["un/o/0.trd.tsk", "debugCurrentOp", [], "un/o/0"])
ses = CGE.CGESession("un/0", [])
ses.setup()
ses.addObj(a)
