'''
Created on Jan 16, 2016

@author: illid_000
'''

import wpilib

class Intake(object):
    '''
    classdocs
    '''


    def __init__(self, firstMotor, secondMotor):
        '''
        Constructor
        '''
        self.motor = wpilib.VictorSP(firstMotor)
        self.motor_out = wpilib.VictorSP(secondMotor)
    
    def set(self, value):
        self.motor.set(value)
        self.motor_out.set(value)