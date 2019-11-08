import maya.cmds as mc
import maya.mel as mm



def mBS():
    oText=mc.textField('original',q=True,tx=True)
    rText=mc.textField('replace',q=True,tx=True)
    
    sel = mc.ls(sl=True)
    print(sel)
    mc.duplicate(sel[0], n='revBlend')
    mc.duplicate(sel[0], n='genBlend')
    mc.blendShape(sel[1],'revBlend', n='tempBlend')
    
    mc.setAttr('revBlend.sx',-1)
    
    mc.select('genBlend','revBlend')
    mm.eval('CreateWrap')
    
    mc.setAttr('tempBlend.'+sel[1],1)
    newBlend = sel[1].replace(oText,rText)
    mc.duplicate('genBlend',n= newBlend)
    mc.delete('genBlend','revBlend','revBlendBase')
    oX=mc.getAttr(sel[1]+'.tx')
    oY=mc.getAttr(sel[1]+'.ty')
    oZ=mc.getAttr(sel[1]+'.tz')
    
    mc.setAttr(newBlend+'.tx', oX+40)
    mc.setAttr(newBlend+'.ty')
    mc.setAttr(newBlend+'.tz')
    
def UI():
    if mc.window('MirrorBlends',exists=True):
        mc.deleteUI('MirrorBlends')
    mc.window('MirrorBlends')
    mc.columnLayout()
    
    mc.text('Text to replace')
    mc.textField('original',tx='L_')
    mc.text('Replacement Text')
    mc.textField('replace',tx='R_')
    mc.button(l='Mirror BlendShape',c='mBS()')
    mc.showWindow('MirrorBlends')
    
    
UI()
    
    
    
    
    
    
    
    
    
    