import maya.cmds as cmds

sel = cmds.ls(sl  = True)

pos = 1   

newName = sel[0]

while pos<5:
    newName=newName.replace(str(pos),str(pos+1))
    cmds.duplicate(name=newName)
    cmds.setAttr(newName+'.tx', pos*5)
    pos=pos+1
    