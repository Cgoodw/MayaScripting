import maya.cmds as mc
import os
import maya.mel as mm

#UI
def UI():
    if mc.window('rigUI',exists=True):
        mc.deleteUI('rigUI')
    mc.window('rigUI')
    mc.columnLayout()
    mc.text(label='')
    mc.textFieldGrp('charname', label = 'Character Name: ')
    mc.button( l = 'Create Default Joints', c='makeJoints()')
    mc.text(label='')
    mc.text(label='Place Joints on Head')
    mc.text(label='')
    mc.text(label='Select the face geometry')
    mc.text(label='')
    mc.button( l = 'Rig and Create Controls', c='makeControls()')
    mc.text(label='')
    mc.text(label='')
    #mc.button( l = 'Import Blend Shapes', c='importBlendShapes()')
    mc.showWindow()
UI()

    #create the joints
def makeJoints():
    mc.select(cl=True)
     #Create Neck
    mc.joint( n = 'lowerNeck_JNT', p= (0,1,-1))
    mc.select(cl=True)
    mc.joint( n = 'upperNeck_JNT', p=(0,5,-0.5))
    mc.select(cl=True)
    #Create the lower jaw
    mc.joint( n = 'lowerJawBase_JNT', p=(0,6.5,0.4))
    mc.select(cl=True)
    mc.joint( n = 'lowerJawEnd_JNT', p=(0,5.5,4.5))
    
    mc.select(cl=True)
   #create the upper jaw
    mc.joint( n = 'upperJawBase_JNT', p=(0,8.5,0.3))
    mc.select(cl=True)
    mc.joint( n = 'upperJawEnd_JNT', p=(0,8.7,4))
    mc.select(cl=True)
    #upper jaw to neck connection
    
    
    #top head joint
    mc.joint( n = 'Head_JNT', p=(0,10,-1))
    

    
def makeControls():
    mc.parent('upperNeck_JNT','lowerNeck_JNT')
    mc.parent('lowerJawBase_JNT','upperNeck_JNT')
    mc.parent('lowerJawEnd_JNT', 'lowerJawBase_JNT')
    mc.parent('upperJawBase_JNT','lowerJawBase_JNT')
    mc.parent('upperJawEnd_JNT','upperJawBase_JNT')
    mc.parent('Head_JNT','upperJawBase_JNT')
    
    charName = mc.textFieldGrp('charname', query = True, text = True)
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
    addDeformers(sel)

def createBoxControl(ctrlName):
    mc.curve(d=1,p=[[-1,1,0],[1,1,0],[1,-1,0],[-1,-1,0],[-1,1,0]],n=ctrlName+'_limitBox')
    mc.circle(n=ctrlName, nr=[0,0,1],r=.1)
    mc.transformLimits(ctrlName,etx=[True,True],ety=[True,True])
    
    mc.textCurves(t=ctrlName,n=ctrlName+'_text')
    mc.setAttr(ctrlName+'_textShape.ty',1.1)
    mc.setAttr(ctrlName+'_textShape.tx',-1)
    mc.setAttr(ctrlName+'_textShape.sy',.3)
    mc.setAttr(ctrlName+'_textShape.sx',.3)
    mc.select(ctrlName+'_textShape',hi=True)
    textSel=mc.ls(sl=True)
        
    
    
    for obj in textSel:
        mc.setAttr(obj+'.template',1)
    mc.parent(ctrlName,ctrlName+'_textShape',ctrlName+'_limitBox')
    mc.setAttr(ctrlName+'.tz',lock=True,k=False,channelBox=False)
    mc.setAttr(ctrlName+'.rx',lock=True,k=False,channelBox=False)
    mc.setAttr(ctrlName+'.ry',lock=True,k=False,channelBox=False)
    mc.setAttr(ctrlName+'.rz',lock=True,k=False,channelBox=False)
    mc.setAttr(ctrlName+'.sz',lock=True,k=False,channelBox=False)
    mc.setAttr(ctrlName+'.sx',lock=True,k=False,channelBox=False)
    mc.setAttr(ctrlName+'.sy',lock=True,k=False,channelBox=False)
    mc.setAttr(ctrlName+'.v',lock=True,k=False,channelBox=False)
    
    
    
def createFaceCTRLS(charName):
    createBoxControl('L_Brow_CTRL_'+charName)
    createBoxControl('R_Brow_CTRL_'+charName)
    mc.setAttr('R_Brow_CTRL_'+charName+'_limitBox.tx',-2.1)
    createBoxControl('L_Eye_CTRL_'+charName)
    mc.setAttr('L_Eye_CTRL_'+charName+'_limitBox.ty',-2.5)
    createBoxControl('R_Eye_CTRL_'+charName)
    mc.setAttr('R_Eye_CTRL_'+charName+'_limitBox.ty',-2.5)
    mc.setAttr('R_Eye_CTRL_'+charName+'_limitBox.tx',-2.1)
    createBoxControl('C_Mouth_CTRL_'+charName)
    mc.setAttr('C_Mouth_CTRL_'+charName+'_limitBox.ty',-6.25)
    mc.setAttr('C_Mouth_CTRL_'+charName+'_limitBox.tx',-1.05)
    mc.setAttr('C_Mouth_CTRL_'+charName+'_limitBox.sx',2)
    mc.setAttr('C_Mouth_CTRL_'+charName+'_limitBox.sx',2)
    mc.curve(d=1,p=[[-3.5,1.5,0],[1.5,1.5,0],[1.5,-9,0],[-3.5,-9,0],[-3.5,1.5,0]],n='Face_CTRL_'+charName)
    mc.textCurves(t=charName,n=charName+'text')
    mc.setAttr(charName+'textShape.tx',-3.5)
    mc.setAttr(charName+'textShape.ty',1.5)
    mc.parent('L_Brow_CTRL_'+charName+'_limitBox','R_Brow_CTRL_'+charName+'_limitBox','L_Eye_CTRL_'+charName+'_limitBox','R_Eye_CTRL_'+charName+'_limitBox',
    'C_Mouth_CTRL_'+charName+'_limitBox',charName+'textShape','Face_CTRL_'+charName)
    
    
def addDeformers(sel):
    sel='headGeo'
    mc.select('R_Brow_GEO',sel)
    mm.eval('CreateWrap')
    mc.select('L_Brow_GEO',sel)
    mm.eval('CreateWrap')
    
    mc.select('CharacterHead')
    
    mc.select('lowerNeck_JNT',add=True)
    mc.bindSkin()
    
    #Set driven keys for each controller
def sdks(charName):
    LorR=['L','R']
    
    for side in LorR:
       
        mc.setDrivenKeyframe(side+'_Eye_GEO.ry',cd=side+'_Eye_CTRL_'+charName+'.tx')
        mc.setAttr(side+'_Eye_CTRL_'+charName+'.tx',-1)
        mc.setAttr(side+'_Eye_GEO.ry',90)
        mc.setDrivenKeyframe(side+'_Eye_GEO.ry',cd=side+'_Eye_CTRL_'+charName+'.tx')
        mc.setAttr(side+'_Eye_CTRL_'+charName+'.tx',1)
        mc.setAttr(side+'_Eye_GEO.ry',-90)
        mc.setDrivenKeyframe(side+'_Eye_GEO.ry',cd=side+'_Eye_CTRL_'+charName+'.tx')
        mc.setAttr(side+'_Eye_CTRL_'+charName+'.tx',0)   
        mc.setAttr(side+'_Eye_GEO.ry',0)
        
        mc.setDrivenKeyframe(side+'_Eye_GEO.rx',cd=side+'_Eye_CTRL_'+charName+'.ty')
        mc.setAttr(side+'_Eye_CTRL_'+charName+'.ty',-1)
        mc.setAttr(side+'_Eye_GEO.rx',90)
        mc.setDrivenKeyframe(side+'_Eye_GEO.rx',cd=side+'_Eye_CTRL_'+charName+'.ty')
        mc.setAttr(side+'_Eye_CTRL_'+charName+'.ty',1)
        mc.setAttr(side+'_Eye_GEO.rx',-90)
        mc.setDrivenKeyframe(side+'_Eye_GEO.rx',cd=side+'_Eye_CTRL_'+charName+'.ty')
        mc.setAttr(side+'_Eye_GEO.rx',0)
        mc.setAttr(side+'_Eye_CTRL_'+charName+'.ty',0)    
         
        
        mc.setDrivenKeyframe(side+'_Brow_GEO.ty',cd=side+'_Brow_CTRL_'+charName+'.ty')
        mc.setAttr(side+'_Brow_CTRL_'+charName+'.ty',-1)
        mc.setAttr(side+'_Brow_GEO.ty',90)
        mc.setDrivenKeyframe(side+'_Brow_GEO.tx',cd=side+'_Brow_CTRL_'+charName+'.ty')
        mc.setAttr(side+'_Brow_CTRL_'+charName+'.ty',1)
        mc.setAttr(side+'_Brow_GEO.ty',-90)
        mc.setDrivenKeyframe(side+'_Brow_GEO.rx',cd=side+'_Brow_CTRL_'+charName+'.ty')
        mc.setAttr(side+'_Brow_GEO.ty',0)
        mc.setAttr(side+'_Brow_CTRL_'+charName+'.ty',0)    
        
    
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
    
def importBlendShapes(sel, charName):
    path=mc.workspace(q=True,rd=True)
    path=path+('scenes/blendShapes/')
    print path
    fileList=os.listdir(path)
    print fileList    
    mc.select('headGeo')
    sel='headGeo'
    mc.blendShape(name = 'faceBlendShapes')
    
    count = 0
    for bs in fileList:
        geoName = bs.split('.')
        geoName = geoName[0]
        realName='headGeoCharacterHead'
        blendParts = bs.split('_')
        mc.file(path+bs,i=True)
        mc.select(cl=True)
        mc.select(realName)
        mc.rename(geoName)
        if count==0:
            geoName=geoName+'1'
        if count==5:
            geoName=geoName+'1'    
        
        print geoName
        mc.blendShape('faceBlendShapes', edit = True, target = (sel, count, geoName, 1.0))
        mc.select('headGeo')
        mc.addAttr( longName= 'Blend_'+geoName, defaultValue=0.0, minValue=0.0, maxValue =1, hidden = False, keyable = True)
        mc.setDrivenKeyframe('faceBlendShapes.'+geoName, cd='headGeo.Blend_'+geoName)
      
        mc.setAttr('headGeo.Blend_'+geoName,1.0)
        mc.setAttr('faceBlendShapes.'+geoName,1.0)
        mc.setDrivenKeyframe('faceBlendShapes.'+geoName, cd='headGeo.Blend_'+geoName)
        mc.setAttr('headGeo.Blend_'+geoName,0)
        mc.setAttr('faceBlendShapes.'+geoName,0)
        mc.setDrivenKeyframe('faceBlendShapes.'+geoName, cd='headGeo.Blend_'+geoName)
        
        mc.delete(geoName)
        count=count+1
def assignBlend(charName,blendParts):
    if blendParts[0]=='C':
        if blendParts[1]=='Mouth':
            if blendParts[1]=='Frown':
                print 'hc'
    if blendParts[0]=='L':
        print 'hl'
    if blendParts[0]=='R':
        print 'hr'
        
    
    
    
    
    
    
    
    
    