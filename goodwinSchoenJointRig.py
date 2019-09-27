import maya.cmds as mc
#list to store the joints and text
jointsList=[]
textList=[]

#create the joint
def jointCreator( name, pos, type, side):
    mc.select(cl=True)
    jointName = side+'_'+name+'_'+type
    mc.joint( n = jointName, p=pos)
    mc.textCurves(n=name,t=name)
    mc.parent(name+'Shape',jointName)
    mc.setAttr(name+'Shape.tx',0)
    mc.setAttr(name+'Shape.ty',0)
    mc.setAttr(name+'Shape.tz',0)
    
    #add to list of joints
    jointsList.append(jointName)
    
    #add text
    textList.append(name+'Shape')


#create all the joints
def makeJoints():
    #LEG
    jointCreator('Hip',[2,6,-2],'BIND','L')
    jointCreator('Knee',[2,4,0],'BIND','L')
    jointCreator('Ankle',[2,1,-0],'BIND','L')
    jointCreator('Ball',[2,0,0],'BIND','L')
    jointCreator('Toes',[2,0,1],'BIND','L')
    
    #TORSO
    jointCreator('Pelvis',[0,6.5,-2],'BIND','C')
    jointCreator('lowerSpine',[0,7,-2.5],'BIND','C')
    jointCreator('lowerChest',[0,9,-2.25],'BIND','C')
    jointCreator('Chest',[0,10,-1.75],'BIND','C')
    jointCreator('upperSpine',[0,12,-2],'BIND','C')
    
    #ARM
    jointCreator('Clavicle',[0,11,-2.25],'BIND','L')
    jointCreator('Shoulder',[3,10.75,-2.25],'BIND','L')
    jointCreator('Elbow',[4,10,-2.25],'BIND','L')
    jointCreator('Wrist',[5,9,-2.25],'BIND','L')
    jointCreator('Palm',[6,8.5,-2],'BIND','L')
    
    #HAND
    jointCreator('IndexA',[6.1,8.16,-1.35],'BIND','L')
    jointCreator('IndexB',[6.7,8.16,-1.07],'BIND','L')
    jointCreator('IndexC',[7.3,7.97,-0.88],'BIND','L')
    jointCreator('MiddleA',[6.47,8.16,-1.69],'BIND','L')
    jointCreator('MiddleB',[7,8.12,-1.67],'BIND','L')
    jointCreator('MiddleC',[7.81,7.98,-1.64],'BIND','L')
    jointCreator('RingA',[6.6,8.16,-2.2],'BIND','L')
    jointCreator('RingB',[7,8.12,-2.28],'BIND','L')
    jointCreator('RingC',[7.65,8,-2.36],'BIND','L')
    jointCreator('PinkieA',[6.53,8.16,-2.66],'BIND','L')
    jointCreator('PinkieB',[7,8.12,-2.86],'BIND','L')
    jointCreator('PinkieC',[7.6,7.98,-3.09],'BIND','L')
    jointCreator('ThumbA',[5.67,8.2,-1.43],'BIND','L')
    jointCreator('ThumbB',[5.9,8.05,-.81],'BIND','L')
    jointCreator('ThumbC',[6.14,7.85,-0.48],'BIND','L')
    
    
    #HEAD
    jointCreator('lowerNeck',[0,12.76,-2],'BIND','L')
    jointCreator('upperNeck',[0,13.8,-2],'BIND','L')
    jointCreator('Head',[0,13.93,-1],'BIND','L')
 
           
#Parent the joints
def createRig():
    mc.delete(textList)
    mc.parent('L_Hip_BIND','C_Pelvis_BIND')
    mc.parent('L_Knee_BIND','L_Hip_BIND')
    mc.parent('L_Ankle_BIND','L_Knee_BIND')
    mc.parent('L_Ball_BIND','L_Ankle_BIND')
    mc.parent('L_Toes_BIND','L_Ball_BIND')
    mc.parent('C_lowerSpine_BIND','C_Pelvis_BIND')
    mc.parent('C_lowerChest_BIND','C_lowerSpine_BIND')
    mc.parent('C_Chest_BIND','C_lowerChest_BIND')
    mc.parent('C_Shoulder_BIND','C_Chest_BIND')
    mc.parent('L_Hip_BIND','C_Pelvis_BIND')
    mc.parent('L_Hip_BIND','C_Pelvis_BIND')
    mc.parent('L_Hip_BIND','C_Pelvis_BIND')
    mc.parent('L_Hip_BIND','C_Pelvis_BIND')
    mc.parent('L_Hip_BIND','C_Pelvis_BIND')
    mc.parent('L_Hip_BIND','C_Pelvis_BIND')
    mc.parent('L_Hip_BIND','C_Pelvis_BIND')
    mc.parent('L_Hip_BIND','C_Pelvis_BIND')
    

    
    #mirror joints



#ui
def UI():
    if mc.window('rigUI',exists=True):
        mc.deleteUI('rigUI')
    mc.window('rigUI')
    mc.columnLayout()
    mc.text(label='STEP 1:')
    mc.text(label='')
    mc.button( l = 'Create Default Joints', c='makeJoints()')
    mc.text(label='___________________')
    mc.text(label='')
    mc.text(label='')
    mc.text(label='STEP 2:')
    mc.text(label='')
    mc.text(label='Move Joints to fit Model')
    mc.text(label='__________________________')
    mc.text(label='')
    mc.text(label='')
    mc.text(label='STEP 3:')
    mc.text(label='')
    mc.button( l = 'Mirror and Rig', c='createRig()')
    mc.text(label='__________________________')
    mc.text(label='')
    mc.showWindow()
UI()