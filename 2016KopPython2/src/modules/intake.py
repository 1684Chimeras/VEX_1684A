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
    
    def set(self, value, value2 = -11):
        if value2 == -11:
            self.motor.set(value * -1)
            self.motor_out.set(value * -2)
        else:
            self.motor.set(value)
            self.motor_out.set(value2)