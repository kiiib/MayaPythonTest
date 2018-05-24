"""
module for making rig control
"""
import maya.cmds as mc

class Control():

    """
    class for building rig control
    """

    def __init__(
                self, 
                prefix = 'new', 
                scale = 1.0, 
                translateTo = '',
                rotateTo = '',
                Parent = '',
                lockChannels =['s','v']
                ):

        ctrlObject = mc.circle( n = prefix + '_ctl', ch = False)[0]
