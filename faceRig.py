import maya.cmds as mc
import os
#UI
def UI():
    if mc.window('rigUI',exists=True):
        mc.deleteUI('rigUI')
    mc.window('rigUI')
    mc.columnLayout()
    mc.text(label='')
    
    mc.text( label='Name' )
    name = mc.textField()
    
    mc.button( l = 'Create Default Joints', c='makeJoints()')
    mc.text(label='')
    mc.text(label='Place Joints on Head')
    mc.text(label='')
    mc.text(label='')
    mc.button( l = 'Rig and Create Controls', c='makeControls()')
    mc.text(label='')
    mc.text(label='')
    mc.button( l = 'Import Blend Shapes', c='importBlendShapes()')
    mc.showWindow()
UI()

    #create the joints
def makeJoints():
     #Create Neck
    mc.joint( n = 'lowerNeck_JNT', p= (0,1,-1))
    mc.joint( n = 'upperNeck_JNT', p=(0,5,-0.5))
    
    
    #Create the lower jaw
    mc.joint( n = 'lowerJawBase_JNT', p=(0,6.5,0.4))
    mc.joint( n = 'lowerJawEnd_JNT', p=(0,5.5,4.5))
    
    mc.select(cl=True)
   #create the upper jaw
    mc.joint( n = 'upperJawBase_JNT', p=(0,8.5,0.3))
    mc.joint( n = 'upperJawEnd_JNT', p=(0,8.7,4))
    
    #upper jaw to neck connection
    mc.parent('upperJawBase_JNT','upperNeck_JNT')
    
    #top head joint
    mc.joint( n = 'Head_JNT', p=(0,10,-1))
    mc.parent('Head_JNT','upperNeck_JNT')

    
def makeControls():
    charName=mc.textField('name',q=True,tx=True)
    sel=mc.ls(sl=True)
    sel=sel[0]
    mc.select(cl=True)
    
    #create the controls
    createControl('BaseCTRL',5,'lowerNeck_JNT',[0,1,0])
    createControl('HeadCTRL',10,'Head_JNT',[0,1,0])
    createControl('NeckCTRL',10,'upperNeck_JNT',[0,1,0])    
    mc.parent('HeadCTRL','NeckCTRL','BaseCTRL')
    mc.parent('upperNeck_JNT','lowerNeck_JNT')
    createFaceCTRLS(charName)
    importBlendShapes(sel,charName)
    sdks(charName)

def createBoxControl(ctrlName):
    mc.curve(d=1,p=[[-1,1,0],[1,1,0],[1,-1,0],[-1,1,0]],n=ctrlName+'_limitBox')
    
    
def createFaceCTRLS(charName):
    createBoxControl('L_Brow_CTRL_'+charName)
    createBoxControl('R_Brow_CTRL_'+charName)
    
    
    
def sdks(charName):
    LorR=['L','R']
    
    for side in LorR:
        mc.setAttr(side+'_Eye_CTRL_'+charName+'.tx',0)
        mc.setDrivenKeyframe(side+'_eyeBall_GEO.ry',cd=side+'_Eye_CTRL_'+charName+'.tx')
        mc.setAttr(side+'_Eye_CTRL_'+charName+'.tx',1)
        mc.setAttr(side+'_eyeBall_GEO.ry',90)
        mc.setDrivenKeyframe(side+'_eyeBall_GEO.ry',cd=side+'_Eye_CTRL_'+charName+'.tx')
        mc.setAttr(side+'_Eye_CTRL_'+charName+'.tx',-1)
        mc.setAttr(side+'_eyeBall_GEO.ry',-90)
        mc.setDrivenKeyframe(side+'_eyeBall_GEO.ry',cd=side+'_Eye_CTRL_'+charName+'.tx')
        mc.setAttr(side+'_Eye_CTRL_'+charName+'.tx',0)    
    
    #function to make the circle controls
def createControl(ctrlName, size, jointName, alignment):
    
    #create circle
    mc.circle(n=ctrlName, nr=alignment)
    CLR = ctrlName.split('_')
    
    #change color based on side
    mc.setAttr(ctrlName+'Shape.overrideEnabled',1)
    mc.setAttr(ctrlName+'Shape.overrideColor',17)
    mc.setAttr(ctrlName+'.sx',size)
    mc.setAttr(ctrlName+'.sy',size)
    mc.setAttr(ctrlName+'.sz',size)
    if jointName==False:
        print ('not Parented')
    else:
        #parent and set position to 0,0,0 to center it
        mc.parent(ctrlName, jointName)
        mc.setAttr(ctrlName+'.tx',0)
        mc.setAttr(ctrlName+'.ty',0)
        mc.setAttr(ctrlName+'.tz',0)
        mc.setAttr(ctrlName+'.rx',0)
        mc.setAttr(ctrlName+'.ry',0)
        mc.setAttr(ctrlName+'.rz',0)
        mc.parent(ctrlName,w=True)
        mc.parent(jointName,ctrlName)
    mc.makeIdentity(apply=True,t=True,r=True,s=True)    
    
def importBlendShapes():
    path=mc.workspace(q=True,rd=True)
    path=path+('scenes/blendShapes/')
    print path
    fileList=os.listdir(path)
    
