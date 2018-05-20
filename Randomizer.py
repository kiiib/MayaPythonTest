from maya import cmds
import random

def createObjects(mode, numObject):
    """ This create object, support Cubes, Spheres, Cylinders and Cones '"""
    objList = []
    
    for n in range(numObject):
        if mode == 'Cube':
            obj = cmds.polyCube()
        elif mode == 'Sphere':
            obj = cmds.polySphere()
        elif mode == 'Cylinder':
            obj = cmds.polyCylinder()
        elif mode == 'Cone':
            obj = cmds.polyCone()
        else: cmds.error("I don't know what to create!")
            
        objList.append(obj[0])

    cmds.select(objList)
            
def randomize(objList = None, minValue = 0, maxValue = 10, axes = 'xyz', mode = 'Absolute'):
    if objList is None:
        objList = cmds.ls(selection = True)
    
    for obj in objList:
        for axis in axes:
            current = 0
            if mode == 'Relative':
                current = cmds.getAttr(obj + '.t%s' % axis)
            
            val = current + random.uniform(minValue, maxValue)
            cmds.setAttr(obj + '.t%s' % axis, val)

        
def showWindow():
    name = "RandomizerWindow"
    if cmds.window(name, query = True, exists = True):
        cmds.deleteUI(name)

    cmds.window(name)
    cmds.showWindow()

    column = cmds.columnLayout()
    cmds.frameLayout(label = "Choose an Object type")

    cmds.columnLayout()
    cmds.radioCollection("objectCreationType")
    cmds.radioButton(label = "Sphere")
    cmds.radioButton(label = "Cube", select = True)
    cmds.radioButton(label = "Cone")

    cmds.intField("numObjects", value = 3)

    cmds.setParent(column)
    frame = cmds.frameLayout("Choose your max range")

    cmds.gridLayout(numberOfColumns = 2, cellWidth = 100)
    
    for axis in 'xyz':
        cmds.text(label = '%s axis' % axis)
        cmds.floatField('%sAxisFiled' % axis, value = random.uniform(0, 10))
    
    cmds.setParent(frame)
    cmds.rowLayout(numberOfColumns = 2)
    cmds.radioCollection("randomMode")
    cmds.radioButton(label = 'Absolute', select = True)
    cmds.radioButton(label = 'Relative')

    cmds.setParent(column)
    cmds.rowLayout(numberOfColumns = 2)
    cmds.button(label = 'Create', command = onCreateClick)
    cmds.button(label = 'Randomize', command = onRandomClick)

def onCreateClick(*args):
    radio = cmds.radioCollection("objectCreationType", query = True, select = True)
    mode = cmds.radioButton(radio, query = True, label = True)

    numObjects = cmds.intField("numObjects", query = True, value = True)

    createObjects(mode, numObjects)
    onCreateClick()

def onRandomClick(*args):
    radio = cmds.radioCollection("randomMode", query = True, select = True)
    mode = cmds.radioButton(radio, query = True, label = True)

    for axis in 'xyz':
        val = cmds.floatField("%sAxisField" % axis) 
        randomize(minValue=val*-1, maxValue=val, mode = mode, axes = axis)
