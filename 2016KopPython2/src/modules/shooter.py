'''
Created on Jan 16, 2016

@author: illid_000
'''

import wpilib
import time
import _thread
import oi
from wpilib import powerdistributionpanel

class Shooter(object):
    '''
    classdocs
    '''


    def __init__(self,camera,driveTrain,params):
        '''
        Constructor
        '''
        #old = -7.6
        
        #number analysis - setpoint 29000, voltage/dec = 11.4/11 hovered at/beneath 29
        #analysis - good good good - 1000 error 29000 set -13 max -11.4 voltage -10.8 dec hovered
        #analysis - 2600, -9.8 voltage, -9.6 dec hovered at 27000 hit the top of the goal woth a new ball 
        #analysis - 24000, -9 voltage -8.7 dec voltage hovered at 24850- 
        #analysis - 24000, -9 voltage -8.7 dec voltage hovered at 24300- hit the bottom of the goal at the back lien of the defense
        #analysis - 24000, -91 voltage -8.8 dec voltage hovered at 24800- hit the bottom of the goal at the back lien of the defense
        self.wheelMaxError = 1000
        self.testSetpoint = 26650
        self.camera = camera
        self.driveTrain = driveTrain
        
        self.maxVoltageSetpoint = -9
        self.voltageSetpoint = -9.7
        self.decVoltageSetpoint = -9.4
        self.motor = wpilib.CANTalon(params)
        self.motor.enableBrakeMode(True)
        self.motor.changeControlMode(wpilib.CANTalon.ControlMode.Voltage)
        self.wasBrake = True
        self.toggleState = False
        self.lastToggleTime = 0
        self.speed = 0
        _thread.start_new_thread( self.periodic, ("Shooter-Update-Thread", "literally nothing",))
        self.pdp = powerdistributionpanel.PowerDistributionPanel()
        
        
        self.motor.reverseOutput(False)
        self.motor.setFeedbackDevice(0) 
    
        
    def getWheelPosition(self):
        return -self.motor.getEncPosition()
    def getWheelVelocity(self):
        return abs(self.motor.getEncVelocity())
    
    def enable(self):
        self.speed = 1
        return
    def getShooterSetpoint(self):
        return self.testSetpoint
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
        
    def setPID(self, value):
        self.speed = value
    
    def wheelGood(self):
        return    abs(self.getShooterSetpoint() - self.getWheelVelocity()) < self.wheelMaxError 
    
    def periodic(self, literally, nothing):
        while(True):
            if wpilib.DriverStation.getInstance().isEnabled():
                self.set(self.speed)
            else:
                self.toggleState = False
                self.speed = 0
                self.set(self.speed)
                
            wpilib.SmartDashboard.putNumber("Wheel Position", self.getWheelPosition())
            wpilib.SmartDashboard.putNumber("Wheel Velocity", self.getWheelVelocity())
            wpilib.SmartDashboard.putNumber("Shooter Amp Draw", self.pdp.getCurrent(3))
            time.sleep(0.005)
    timeToSpin = 5.33
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
            '''
            if self.lastToggleTime + Shooter.timeToFire > time.time():
                self.motor.set(self.maxVoltageSetpoint)
            else:
                if self.lastToggleTime + Shooter.timeToSpin < time.time():
                    #print("yes {} {}".format(self.lastToggleTime, time.time()))
                    oi.OI.driverVibrate(0.7,0.7)
                else:
                    #print("no {} {}".format(self.lastToggleTime, time.time()))
                    oi.OI.driverVibrate(0,0)
                self.motor.set(value * self.voltageSetpoint)
            '''
            set = 0
            if abs(self.getShooterSetpoint() - self.getWheelVelocity()) > self.wheelMaxError:
                oi.OI.driverVibrate(0,0)
                if self.getWheelVelocity() > self.getShooterSetpoint():
                    print("DEC VELOCITY")
                    set = self.decVoltageSetpoint
                    self.motor.set(self.decVoltageSetpoint)
                else:
                    print("MAX VELOCITY {} {}".format(self.getWheelVelocity(), self.getShooterSetpoint()))
                    set = self.maxVoltageSetpoint
                    self.motor.set(self.maxVoltageSetpoint)
            else:
                print("STEADY VELOCITY")
                if self.driveTrain.ready_to_shoot():
                    oi.OI.driverVibrate(0.7,0.7)
                else:
                    oi.OI.driverVibrate(0,0)
                set = self.voltageSetpoint
                self.motor.set(self.voltageSetpoint)
                
            wpilib.SmartDashboard.putNumber("Shooter Actual Setpoint",  self.motor.get())
            wpilib.SmartDashboard.putNumber("Shooter Desired Setpoint",  set)
        else:
            oi.OI.driverVibrate(0,0)
            self.motor.set(value * self.voltageSetpoint)