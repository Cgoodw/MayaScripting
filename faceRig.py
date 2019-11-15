import maya.cmds as mc

#UI
def UI():
    if mc.window('rigUI',exists=True):
        mc.deleteUI('rigUI')
    mc.window('rigUI')
    mc.columnLayout()
    mc.text(label='')
    mc.button( l = 'Create Default Joints', c='makeJoints()')
    mc.text(label='')
    mc.text(label='')
    mc.text(label='')
    #mc.button( l = 'Create Controls', c='makeJoints()')
    mc.text(label='')
    mc.text(label='')
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
    
    createControl('BaseCTRL',5,'lowerNeck_JNT',[0,1,0])
    mc.parent('lowerNeck_JNT','BaseCTRL')
    
    createControl('HeadCTRL',10,'Head_JNT',[0,1,0])
    mc.parent('Head_JNT','HeadCTRL')
    
    createControl('NeckCTRL',10,'upperNeck_JNT',[0,1,0])
    mc.parent('upperNeck_JNT','NeckCTRL')
    
    mc.parent('HeadCTRL','NeckCTRL','BaseCTRL')
    
    #creating the circle controls
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
    mc.makeIdentity(apply=True,t=True,r=True,s=True)