'''
Created on Jan 16, 2016

@author: illid_000
'''

import wpilib

class DriveTrain(object):
    '''
    classdocs
    '''


    def __init__(self, leftDrive, rightDrive, leftB, rightB):
        '''
        Constructor
        '''
    
        self.robotDrive = wpilib.RobotDrive(leftDrive, leftB, rightDrive, rightB)
        
        #self.robotDrive.setInvertedMotor(wpilib.RobotDrive.MotorType.kFrontLeft, True)
        #self.robotDrive.setInvertedMotor(wpilib.RobotDrive.MotorType.kRearRight, True)
        
    def arcadeDrive(self, move, rotate):
        if abs(move) > 0.98:
            if move > 0:
                move = 1
            else:
                move = -1
        if abs(rotate) > 0.98:
            if rotate > 0:
                rotate = 1
            else:
                rotate = -1

        self.robotDrive.arcadeDrive(move, rotate, True)