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

def createControl(ctrlName, size, jointName, alignment):
    mc.circle(n=ctrlName, nr=alignment)
    CLR = ctrlName.split('_')
    print CLR
    mc.setAttr(ctrlName+'Shape.overrideEnabled',1)
    if CLR[0]=='C':
        mc.setAttr(ctrlName+'Shape.overrideColor',17)
    elif CLR[0]=='L':
        mc.setAttr(ctrlName+'Shape.overrideColor',6)
    elif CLR[0]=='R':
        mc.setAttr(ctrlName+'Shape.overrideColor',13)
    mc.setAttr(ctrlName+'.sx',size)
    mc.setAttr(ctrlName+'.sy',size)
    mc.setAttr(ctrlName+'.sz',size)
    if jointName==False:
        print ('not Parented')
    else:
        mc.parent(ctrlName, jointName)
        mc.setAttr(ctrlName+'.tx',0)
        mc.setAttr(ctrlName+'.ty',0)
        mc.setAttr(ctrlName+'.tz',0)
        mc.setAttr(ctrlName+'.rx',0)
        mc.setAttr(ctrlName+'.ry',0)
        mc.setAttr(ctrlName+'.rz',0)
        mc.parent(ctrlName,w=True)
    mc.makeIdentity(apply=True,t=True,r=True,s=True)


def createRigControl():
    createControl('C_Master_CTRL',5,False,[0,1,0])
    createControl('C_COG_CTRL',4,'C_Pelvis_BIND',[0,1,0])
    createControl('C_Chest_CTRL',4,'C_upperSpine_BIND',[0,1,0])
    createControl('C_Head_CTRL',4,'C_Head_BIND',[0,1,0])
    createControl('R_Arm_CTRL',2,'R_Wrist_BIND',[1,0,0])
    createControl('L_Arm_CTRL',2,'L_Wrist_BIND',[1,0,0])
    createControl('R_Foot_CTRL',2,'R_Ankle_BIND',[0,1,0])
    createControl('L_Foot_CTRL',2,'L_Ankle_BIND',[0,1,0])
    mc.parent('C_COG_CTRL','C_Chest_CTRL','C_Head_CTRL','R_Arm_CTRL','L_Arm_CTRL','L_Foot_CTRL','R_Foot_CTRL','C_Master_CTRL')
    mc.parent('C_Chest_CTRL','C_Head_CTRL','C_COG_CTRL')
    mc.parent('C_Head_CTRL','C_Chest_CTRL')
    mc.select(cl= True)
 
    
    mc.select(cl=True)
    #Reverse Foot
    revFoot('L')
    revFoot('R')
    createIKs()
    
    
    
    #Group controls
    mc.group('L_Arm_IK','R_Arm_IK','L_Toes_IK','R_Toes_IK','L_Ankle_IK','R_Ankle_IK', n='IK_Handles')
    mc.group('C_Master_CTRL','R_Foot_CTRL','L_Foot_CTRL', n='Controls')
    mc.group('L_ReverseFootBall_BIND','L_ReverseFootToes_BIND','L_ReverseFootAnkle_BIND','L_ReverseFootHeel_BIND','R_ReverseFootBall_BIND','R_ReverseFootToes_BIND','R_ReverseFootAnkle_BIND','R_ReverseFootHeel_BIND', n='ReverseFoot')
    mc.group('C_Pelvis_BIND','ReverseFoot', n='Joints')
    mc.group('IK_Handles','Controls','Joints', n='Character_Rig')
    
    #parent controls
    mc.parentConstraint('L_Arm_CTRL','L_Arm_IK')
    mc.orientConstraint('L_Arm_CTRL','L_Wrist_BIND')
    mc.parentConstraint('R_Arm_CTRL','R_Arm_IK')
    mc.orientConstraint('R_Arm_CTRL','R_Wrist_BIND', mo=True)
    mc.parentConstraint('L_Foot_CTRL','L_Foot_IK')
    mc.parentConstraint('R_Foot_CTRL','R_Foot_IK')
    mc.parentConstraint('C_COG_CTRL','C_Pelvis_BIND')
    mc.parentConstraint('C_Chest_CTRL','C_Chest_BIND')
    mc.parentConstraint('C_Head_CTRL','C_Head_BIND', mo=True)
    
   
    
    
def createIKs():
    
    
    mc.ikHandle(n='R_Arm_IK',sj='R_Shoulder_BIND', ee='R_Wrist_BIND',p=2,w=.5)
    mc.ikHandle(n='L_Arm_IK',sj='L_Shoulder_BIND', ee='L_Wrist_BIND',p=2,w=.5)
  #  mc.ikHandle(n='R_Foot_IK',sj='R_Hip_BIND', ee='R_Ankle_BIND',p=2,w=.5)
  #  mc.ikHandle(n='L_Foot_IK',sj='L_Hip_BIND', ee='L_Ankle_BIND',p=2,w=.5)
    
    
    mc.ikHandle(n='L_Ankle_IK',sj='L_Hip_BIND', ee='L_Ankle_BIND',p=2,w=.5)
    mc.ikHandle(n='R_Ankle_IK',sj='R_Hip_BIND', ee='R_Ankle_BIND',p=2,w=.5)
    mc.ikHandle(n='L_Toes_IK',sj='L_Ball_BIND', ee='L_Toes_BIND',p=2,w=.5)
    mc.ikHandle(n='R_Toes_IK',sj='R_Ball_BIND', ee='R_Toes_BIND',p=2,w=.5)
    mc.ikHandle(n='L_Ankle_IK',sj='L_Toes_BIND', ee='L_Ball_BIND',p=2,w=.5)
    mc.ikHandle(n='R_Ankle_IK',sj='R_Toes_ BIND', ee='R_Ball_BIND',p=2,w=.5)
    
def revFoot(side):
    #REVERSE FOOT
    mc.joint(n=side+'_ReverseFootBall_BIND')
    mc.joint(n=side+'_ReverseFootToes_BIND')
    mc.joint(n=side+'_ReverseFootAnkle_BIND')
    mc.joint(n=side+'_ReverseFootHeel_BIND')
        
    mc.parent(side+'_ReverseFootAnkle_BIND',side+'_Ankle_BIND')
    mc.parent(side+'_ReverseFootHeel_BIND',side+'_Ankle_BIND')
    mc.parent(side+'_ReverseFootToes_BIND',side+'_Toes_BIND')
    mc.parent(side+'_ReverseFootBall_BIND',side+'_Ball_BIND')
    
    #Ankle
    mc.setAttr(side+'_ReverseFootAnkle_BIND'+'.tx',0)
    mc.setAttr(side+'_ReverseFootAnkle_BIND'+'.ty',0)
    mc.setAttr(side+'_ReverseFootAnkle_BIND'+'.tz',0)
    mc.select(cl=True)
    mc.parent(side+'_ReverseFootAnkle_BIND',w=True)
    
    #Ball
    
    mc.setAttr(side+'_ReverseFootBall_BIND'+'.tx',0)
    mc.setAttr(side+'_ReverseFootBall_BIND'+'.ty',0)
    mc.setAttr(side+'_ReverseFootBall_BIND'+'.tz',0)
    mc.select(cl=True)
    mc.parent(side+'_ReverseFootBall_BIND',w=True)
    
    #Toes
    mc.setAttr(side+'_ReverseFootToes_BIND'+'.tx',0)
    mc.setAttr(side+'_ReverseFootToes_BIND'+'.ty',0)
    mc.setAttr(side+'_ReverseFootToes_BIND'+'.tz',0)
    mc.select(cl=True)
    mc.parent(side+'_ReverseFootToes_BIND',w=True)
    
    #Heel
    mc.setAttr(side+'_ReverseFootHeel_BIND'+'.tx',0)
    mc.setAttr(side+'_ReverseFootHeel_BIND'+'.ty',0)
    mc.setAttr(side+'_ReverseFootHeel_BIND'+'.tz',0)
    mc.select(cl=True)
    mc.parent(side+'_ReverseFootHeel_BIND',w=True)
    mc.setAttr(side+'_ReverseFootHeel_BIND'+'.ty',0)
    
   # A->B
    #B->T
    #T->H
    
    #Parent
   # mc.parent(side+'_Ankle_IK',side+'_ReverseFootBall_BIND')
   # mc.parent(side+'_Ball_IK',side+'_ReverseFootToes_BIND')
   # mc.parent(side+'_Toes_IK',side+'_ReverseFootHeel_BIND')
    
    mc.parent(side+'_ReverseFootAnkle_BIND',side+'_ReverseFootBall_BIND')
    mc.parent(side+'_ReverseFootBall_BIND',side+'_ReverseFootToes_BIND')
    mc.parent(side+'_ReverseFootToes_BIND',side+'_ReverseFootHeel_BIND')
    
    
   
    

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
    jointCreator('lowerNeck',[0,12.76,-2],'BIND','C')
    jointCreator('upperNeck',[0,13.8,-2],'BIND','C')
    jointCreator('Head',[0,13.93,-1],'BIND','C')
 
           
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
    mc.parent('L_Clavicle_BIND','C_Chest_BIND')
    mc.parent('L_Shoulder_BIND','L_Clavicle_BIND')
    mc.parent('L_Elbow_BIND','L_Shoulder_BIND')
    mc.parent('L_Wrist_BIND','L_Elbow_BIND')
    mc.parent('L_Palm_BIND','L_Wrist_BIND')
    mc.parent('L_ThumbA_BIND','L_PinkieA_BIND','L_IndexA_BIND','L_MiddleA_BIND','L_RingA_BIND','L_Palm_BIND')
    mc.parent('L_ThumbC_BIND','L_ThumbB_BIND','L_ThumbA_BIND')
    mc.parent('L_PinkieC_BIND','L_PinkieB_BIND','L_PinkieA_BIND')
    mc.parent('L_MiddleC_BIND','L_MiddleB_BIND','L_MiddleA_BIND')
    mc.parent('L_RingC_BIND','L_RingB_BIND','L_RingA_BIND')
    mc.parent('L_IndexC_BIND','L_IndexB_BIND','L_IndexA_BIND')
    
   
    mc.parent('C_upperSpine_BIND','C_Chest_BIND')
    
    mc.parent('C_lowerNeck_BIND','C_upperSpine_BIND')
   
    mc.parent('C_upperNeck_BIND','C_lowerNeck_BIND')
    mc.parent('C_Head_BIND','C_upperNeck_BIND')
    
    #mirror joints
    mc.mirrorJoint('L_Hip_BIND', mirrorYZ=True,mirrorBehavior=True, sr=['L','R'])
    mc.mirrorJoint('L_Clavicle_BIND', mirrorYZ=True,mirrorBehavior=True, sr=['L','R'])
    
    createRigControl()


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
