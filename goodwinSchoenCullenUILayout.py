import maya.cmds as cmds
import sys
import functools

def UI():
	if cmds.window("UI", exists = True):
		cmds.deleteUI("UI")
	window = cmds.window("UI", title = "Object Grid Maker", w = 350, h = 500, mnb = False, mxb = False, sizeable = False)
	cmds.columnLayout()
	cmds.text(label='Object Grid Maker')
	cmds.text(label='')
	cmds.text(label='Please Select an Object')
	cmds.text(label='')
	cmds.textField('ObjPrefix',pht='Object Prefix')
	cmds.text(label='')
	cmds.textField('ObjSuffix',pht='Object Suffix')
	cmds.text(label='')
	cmds.text(label='Number of Total Objects')
	cmds.intField('ObjNum', value=5)	
	cmds.text(label='')
	cmds.text(label='Grid Length')
	cmds.text(label='1          5             10')
	cmds.intSlider('ObjNumL', min=1, max=10, value=1, step=1 )
	cmds.text(label='')
	cmds.text(label='Grid Depth')
	cmds.text(label='1          5             10')
	cmds.intSlider('ObjNumD', min=1, max=10, value=5, step=1 )
	cmds.text(label='')
	cmds.text(label='Starting Coordinates')
	cmds.text(label='X')
	cmds.intField('StartX',value=0)
	cmds.text(label='Y')
	cmds.intField('StartY',value=0)
	cmds.text(label='Z')
	cmds.intField('StartZ',value=0)
	
	cmds.button(label='Make a grid', command='gridFunc()')
	cmds.showWindow(window)
	
UI()


def gridFunc():
	sel = cmds.ls(sl  = True)
	
	posX =  cmds.intField('StartX',q=True,value=True)   
	posY =  cmds.intField('StartY',q=True,value=True)
	posZ =  cmds.intField('StartZ',q=True,value=True)
	
	numX =  0 
	numY =  0
	numZ =  0
			
	total = cmds.intField('ObjNum',q=True,value=True)
	totalx= cmds.intSlider('ObjNumL',q=True,value=True)
	totalz= cmds.intSlider('ObjNumD',q=True,value=True)
	
	count = 1
	newName = cmds.textField('ObjPrefix',q=True,text=True)+sel[0]+ cmds.textField('ObjSuffix',q=True,text=True)
	
	while count<= total:
		newName=newName.replace(str(count),str(count+1))
		cmds.duplicate(name=newName)
		numX+=1
		cmds.setAttr(newName+'.tx', posX+numX*2)
		cmds.setAttr(newName+'.tz', posZ+numZ*2)
		cmds.setAttr(newName+'.ty', posY+numY*2)
		if numX>totalx-1:
			numX=0
			numZ+=1
		if numZ>totalz-1:
			numZ=0
			numX+=1
		count=count+1
		
		