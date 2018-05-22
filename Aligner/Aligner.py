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
        pass

    def buildUI(self):
        # Add radio buttons for axis

        # Add radio buttons for mode

        # add apply button

        pass

    def onApplyClick(self, *args):
        # get the axis

        # get the mode

        #call the alignment function

        pass