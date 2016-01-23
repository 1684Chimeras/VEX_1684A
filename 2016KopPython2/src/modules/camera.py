'''
Created on Jan 23, 2016

@author: Arhowk
'''

import wpilib
from networktables import NetworkTable

class Camera(object):
    '''
    classdocs
    '''

    def processImage(self):
        #print("What idiot just called the camera.processImage function?")
        return
    
    def getRotationOffset(self):
        return 0.0
    
    def getZOffset(self):
        return 0.0

    def __init__(self):
        '''
        Constructor
        '''
        self.table = NetworkTable.getTable("GRIP").getTable("targetDetection")
        