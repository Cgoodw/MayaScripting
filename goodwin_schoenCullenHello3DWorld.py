import maya.cmds as cmds
import sys


cmds.textCurves(t='Hello 3D World', n='text')
cmds.planarSrf(n='text')

print 'Hello 3D Digital Design'
sys.stdout.write('Hello 3D World')