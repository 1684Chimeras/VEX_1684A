'''
Created on Jan 16, 2016

@author: illid_000
'''

import wpilib

class DriveTrain(object):
    '''
    classdocs
    '''


    def __init__(self, leftDrive, rightDrive):
        '''
        Constructor
        '''
        self.robotDrive = wpilib.RobotDrive(leftDrive, rightDrive)
        
    def arcadeDrive(self, move, rotate):
        self.robotDrive.arcadeDrive(move, rotate, True)