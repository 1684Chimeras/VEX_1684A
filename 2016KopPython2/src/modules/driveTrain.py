'''
Created on Jan 16, 2016

@author: illid_000
'''

import wpilib

class DriveTrain(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        self.robotDrive = wpilib.RobotDrive(params[0], params[1])
        
    def arcadeDrive(self, move, rotate):
        self.robotDrive.arcadeDrive(move, rotate, True)