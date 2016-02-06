'''
Created on Jan 16, 2016

@author: illid_000
'''

import wpilib
import time
import _thread

class Shooter(object):
    '''
    classdocs
    '''


    def __init__(self,  params):
        '''
        Constructor
        '''
        self.voltageSetpoint = -7.6
        self.motor = wpilib.CANTalon(params)
        self.motor.enableBrakeMode(True)
        self.motor.changeControlMode(wpilib.CANTalon.ControlMode.Voltage)
        self.wasBrake = True
        self.toggleState = False
        self.lastToggleTime = 0
        self.speed = 0
        _thread.start_new_thread( self.periodic, ("Shooter-Update-Thread", "literally nothing",))
        
    def enable(self):
        self.speed = 1
        return
    
    def disable(self):
        self.speed = 0
    timeToFire = 2
    def changeOnToggle(self, value):
        if abs(value) > 0.5:
            if not self.toggleState:
                self.lastToggleTime = time.time()
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
                
            time.sleep(0.005)
    
    def set(self, value):
        if(value > 0.1 or value < -0.1):
            if(self.wasBrake):
                self.wasBrake = False
                self.motor.enableBrakeMode(False)
        else:
            if(not self.wasBrake):
                self.wasBrake = True
                self.motor.enableBrakeMode(True)
        if value != 0:
            if self.lastToggleTime + Shooter.timeToFire > time.time():
                print("FULL SPEED")
                self.motor.set(self.voltageSetpoint)
            else:
                print("MEH SPEED")
                self.motor.set(value * self.voltageSetpoint)
        else:
            self.motor.set(value * self.voltageSetpoint)