'''
Created on Jan 16, 2016

@author: illid_000
'''

import wpilib

class Shooter(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        self.motor = wpilib.CANTalon(params)
        self.motor.enableBrakeMode(True)
        self.motor.changeControlMode(wpilib.CANTalon.ControlMode.Voltage)
        self.wasBrake = True
        
    def set(self, value):
        if(value > 0.1 or value < -0.1):
            if(self.wasBrake):
                self.wasBrake = False
                self.motor.enableBrakeMode(False)
        else:
            if(not self.wasBrake):
                self.wasBrake = True
                self.motor.enableBrakeMode(True)
                
        self.motor.set(value)