import maya.cmds as cmds

sel = cmds.ls(sl  = True)

posX = 0   
posY = 0
posZ = 0
count = 1
newName = sel[0]

while posX<5:
    while posY<5:
        while posZ<5:
            newName=newName.replace(str(count),str(count+1))
            cmds.duplicate(name=newName)
            cmds.setAttr(newName+'.tx', posX*5)
            cmds.setAttr(newName+'.ty', posY*5)
            cmds.setAttr(newName+'.tz', posZ*5)
            count=count+1
            posZ=posZ+1
        posY=posY+1
        posZ=0
    posX=posX+1
    posY=0
    