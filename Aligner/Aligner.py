from maya import cmds

def align(nodes = None, axis = 'x', mode = 'mid'):
    # default node to selection if nothing provided
    if not nodes:
        nodes = cmds.ls(sl = True) # sl, selection
    
    if not nodes:
        cmds.error('Nothing selected or provied')
    
    #print nodes

    bboxes = {}
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

    values = []

    # gets the dimension of our objects
    for node in nodes:
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

        cmds.rowLayout(numberOfColumns = 3)
        cmds.radioCollection()
        self.xAsis = cmds.radioButton(label = 'x', select = True)
        self.yAsis = cmds.radioButton(label = 'y')
        self.zAsis = cmds.radioButton(label = 'z')

        # Add radio buttons for mode
        cmds.setParent(column)

        cmds.frameLayout(label = "Choose where to align")

        cmds.rowLayout(numberOfColumns = 3)
        cmds.radioCollection()
        self.minMode = cmds.radioButton(label = 'min')
        self.midMode = cmds.radioButton(label = 'mid', select = True)
        self.maxMode = cmds.radioButton(label = 'max')
        
        # add apply button
        cmds.setParent(column)
        cmds.button(label = 'Align', command = self.onApplyClick)

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
        