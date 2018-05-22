from maya import cmds
from functools import partial

def align(nodes = None, axis = 'x', mode = 'mid'):
    # default node to selection if nothing provided
    if not nodes:
        nodes = cmds.ls(sl = True) # sl, selection
    
    if not nodes:
        cmds.error('Nothing selected or provied')
    
    _nodes = []
    for node in nodes:
        if '.f[' in node:
            node = cmds.polyListComponentConversion(node, fromFace = True, toVertex = True)
        elif '.e[' in node:
            node = cmds.polyListComponentConversion(node, fromEdge = True, toVertex = True)
        
        cmds.select(node)
        node = cmds.ls(sl = True, fl = True)    #sl, select. fl, flatten

        _nodes.extend(node)

    nodes = _nodes

    if axis == 'x':
        start = 0
    elif axis == 'y':
        start = 1
    elif axis == 'z':
        start = 2
    else:
        cmds.error('Unknown Axis')

    minMode = mode == 'min'
    maxMode = mode == 'max'
    midMode = mode == 'mid'

    bboxes = {}
    values = []

    # gets the dimension of our objects
    for node in nodes:
        if '.vtx[' in node:
            ws = cmds.xform(node, q = True, t = True, ws = True)    # q, query. t, tranform. ws, world space
            minValue = midValue = maxValue = ws[start]
        else:
            bbox = cmds.exactWorldBoundingBox(node)   # bbox, bounding box

            minValue = bbox[start]
            maxValue = bbox[start + 3]
            midValue = (minValue + maxValue) / 2

        bboxes[node] = (minValue, midValue, maxValue)

        #print minValue, maxValue, midValue
        if minMode:
            values.append(minValue)
        elif maxMode:
            values.append(maxValue)
        else:
            values.append(midValue)

    # we calculate the alignment point
    if minMode:
        target = min(values)
    elif maxMode:
        target = max(values)
    else:
        target = sum(values) / len(values)  # get the average

    #print target

    # figure out the distance to the target
    for node in nodes:
        bbox = bboxes[node]
        minValue, midValue, maxValue = bbox

        ws = cmds.xform(node, query = True, translation = True, ws = True) # ws, world space
        width = maxValue - minValue
        if minMode:
            distance = minValue - target
            ws[start] = (minValue - distance) + width / 2
        elif maxMode:
            distance = target - maxValue
            ws[start] = (maxValue + distance) - width / 2
        else:
            distance = target - midValue
            ws[start] = midValue + distance

    # move the objecct to the target
        cmds.xform(node, translation = ws, ws = True)

    pass

class Aligner(object):
    def __init__(self):
        name = "Aligner"
        if cmds.window(name, query = True, exists = True):
            cmds.deleteUI(name)

        window = cmds.window(name)
        self.buildUI()
        cmds.showWindow()
        cmds.window(window, e = True, resizeToFitChildren = True)  # e, edit.
    def buildUI(self):
        column = cmds.columnLayout()
        # Add radio buttons for axis
        cmds.frameLayout(label = "Choose an axis")

        cmds.radioCollection()
        self.xAsis = cmds.radioButton(label = 'x', select = True)
        self.yAsis = cmds.radioButton(label = 'y')
        self.zAsis = cmds.radioButton(label = 'z')

        cmds.gridLayout(numberOfColumns = 3, cellWidth = 50)
        createIconButton('XAxis.png', command=partial(self.onOptionClick, self.xAsis))
        createIconButton('YAxis.png', command=partial(self.onOptionClick, self.yAsis))
        createIconButton('ZAxis.png', command=partial(self.onOptionClick, self.zAsis))

        # Add radio buttons for mode
        cmds.setParent(column)

        cmds.frameLayout(label = "Choose where to align")

        cmds.radioCollection()
        self.minMode = cmds.radioButton(label = 'min')
        self.midMode = cmds.radioButton(label = 'mid', select = True)
        self.maxMode = cmds.radioButton(label = 'max')

        cmds.gridLayout(numberOfColumns = 3, cellWidth = 50)
        createIconButton('MinAxis.png', command=partial(self.onOptionClick, self.minMode))
        createIconButton('MidAxis.png', command=partial(self.onOptionClick, self.midMode))
        createIconButton('MaxAxis.png', command=partial(self.onOptionClick, self.maxMode))
        
        # add apply button
        cmds.setParent(column)
        cmds.button(label = 'Align', command = self.onApplyClick, bgc = (0.2, 0.5, 0.9))

    def onOptionClick(self, opt):
        cmds.radioButton(opt, edit = True, select = True)

    def onApplyClick(self, *args):
        # get the axis
        if cmds.radioButton(self.xAsis, q = True, select = True):
            axis = 'x'
        elif cmds.radioButton(self.yAsis, q = True, select = True):
            axis = 'y'
        else:
            axis = 'z'
        
        # get the mode
        if cmds.radioButton(self.minMode, q = True, select = True):
            mode = 'min'
        elif cmds.radioButton(self.midMode, q = True, select = True):
            mode = 'mid'
        else:
            mode = 'max'
        #call the alignment function
        align(axis = axis, mode = mode)
        
def getIcon(icon):
    import os
    scripts = os.path.dirname(__file__)
    icons = os.path.join(scripts, 'icons')

    icon = os.path.join(icons, icon)
    return icon

def createIconButton(icon, command = None):
    if command:
        cmds.iconTextButton(image1 = getIcon(icon), width = 50, height = 50, command = command)
    else:
        cmds.iconTextButton(image1 = getIcon(icon), width = 50, height = 50)
