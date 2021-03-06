'''
Created on Jan 19, 2016

@author: Arhowk
'''

from autons._base_auton import BaseAutonRoutine
import wpilib

class SpinRoutine(BaseAutonRoutine):
    '''
    classdocs
    '''


    def __init__(self, deg, timeout = -1, resetGyro=True):
        self.deg = deg
        self.resetGyro = resetGyro
        if timeout != -1:
            self.setTimeout(timeout)
    
    def initialize(self):
        wpilib.DriverStation.reportError("\Rotate Offset: {}".format(self.camera.getRotationOffset()))
        if self.resetGyro:
            self.drive_train.pid_rotate(self.deg)
        else:
            wpilib.DriverStation.reportError("\Gyro Offset: {}".format(self.drive_train.gyro.getAngle()))
            self.drive_train.pid_rotate(self.deg + self.drive_train.gyro.getAngle())
        
    def periodic(self):
        self.drive_train.pid_periodic(0)
        
    def onFinished(self):
        self.drive_train.stop()