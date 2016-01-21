'''
Created on Jan 16, 2016

@author: illid_000
'''

import wpilib
import _thread

class Shooter(object):
    '''
    classdocs
    '''


    def __init__(self,  params):
        '''
        Constructor
        '''
        self.motor = wpilib.CANTalon(params)
        self.motor.enableBrakeMode(True)
        self.motor.changeControlMode(wpilib.CANTalon.ControlMode.Voltage)
        self.wasBrake = True
        self.toggleState = False
        _thread.start_new_thread( self.periodic, ("Shooter-Update-Thread", "literally nothing",))
        
    def enable(self):
        self.speed = 1
        return
    
    def disable(self):
        self.speed = 0
    
    def changeOnToggle(self, value):
        if abs(value) > 0.5:
            if self.toggleState:
                self.speed = 1 - self.speed
            self.toggleState = True
        else:
            self.toggleState = False
    
    def toggle(self):
        self.speed = 1 - self.speed
        
    def periodic(self, literally, nothing):
        while(True):
            if wpilib.DriverStation.getInstance().isEnabled():
                self.set(self.speed)
            else:
                self.toggleState = False
                self.speed = 0
                self.set(self.speed)
    
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