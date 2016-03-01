'''
Created on Jan 23, 2016

@author: Arhowk
'''

import wpilib
import subprocess
import _thread
from networktables import NetworkTable
from networktables import NumberArray

class Camera(object):
    '''
    classdocs
    '''
    
    #150/full power- center
    camera_width = 240
    camera_height = 320
    center_x = 122
    center_y = 150
    angle_of_camera = 67
    degrees_per_x_error = -angle_of_camera / camera_width
    time_per_y_error = 1
    
    def _getArray(self, key):
        beta = NumberArray()
        self.table.retrieveValue(key, beta)
        return beta

    def processImage(self):
        #print("What idiot just called the camera.processImage function?")
        self.rotateError = 0
        try:
            beta = self._getArray("area")
            x = self._getArray("centerX")
            y = self._getArray("centerY") 
            self.largestArea = 0
            self.largestIndex = -1
            for index in range(len(beta)):
                if beta[index] > self.largestArea:
                    self.largestIndex = index
                    self.largestArea = beta[index]
            if self.largestIndex != -1:
                wpilib.SmartDashboard.putNumber("Largest Area", beta[self.largestIndex])
                wpilib.SmartDashboard.putNumber("Largest x", x[self.largestIndex])
                wpilib.SmartDashboard.putNumber("Largest y", y[self.largestIndex])
                wpilib.SmartDashboard.putNumber("X Error", self.center_x - x[self.largestIndex])
                wpilib.SmartDashboard.putNumber("Rotate Error", self.degrees_per_x_error * (self.center_x - x[self.largestIndex]))
                wpilib.SmartDashboard.putNumber("Y Error", self.center_y - y[self.largestIndex])
                
                self.rotateError = self.degrees_per_x_error * (self.center_x - x[self.largestIndex])
                self.y = y[self.largestIndex]
            return
        except KeyError:
            return
        except IndexError:
            return
    
    def getPixelXOffset(self):
        
        return
    
    def getY(self):
        return self.y / self.camera_height
    
    def getIntakeOffset(self):
        pass
    
    def getRotationOffset(self):
        return self.rotateError
    
    def getZOffset(self):
        return 0.0
    
    def startProcess(self, literally, nothing):
        print("CALL BEGIN")
        subprocess.call(["/usr/local/frc/JRE/bin/java", "-jar", "/home/lvuser/grip.jar", "/home/lvuser/project.grip"])
        print("CALL END")

    def __init__(self):
        '''
        Constructor
        '''
        #start GRIP
        #_thread.start_new_thread( self.startProcess, ("Grip-Thread", "literally nothing",))
        
        self.largestArea = 0
        self.largestIndex = -1
        #print("Setting IP Address...")
        #print("Getting Table...")
        self.table = NetworkTable.getTable("/GRIP/targetDetection")
        #print("Done!")