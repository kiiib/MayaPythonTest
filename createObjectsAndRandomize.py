from maya import cmds
import random

def createObjects(mode, numObject):
    objList = []
    
    for n in range(numObject):
        if mode == 'Cube':
            obj = cmds.polyCube()
        elif mode == 'Sphere':
            obj = cmds.polySphere()
        elif mode == 'Cone':
            obj = cmds.polyCone()
        else:
            cmds.error("I don't know what to create!")
            
        objList.append(obj[0])
        
    return objList
            
def randomize(objList, minValue = 0, maxValue = 50):
    for obj in objList:
        cmds.setAttr(obj + '.tx', random.randint(minValue, maxValue))
        cmds.setAttr(obj + '.ty', random.randint(minValue, maxValue))
        cmds.setAttr(obj + '.tz', random.randint(minValue, maxValue))
        
objList = createObjects('Cone', 5)
randomize(objList, maxValue = 10)