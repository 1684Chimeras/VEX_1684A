'''
Created on Jan 16, 2016

@author: illid_000
'''

import wpilib
import math
from email._header_value_parser import AngleAddr
from wpilib.smartdashboard import SmartDashboard

class DriveTrain(object):
    '''
    classdocs
    '''


    def __init__(self, leftDrive, rightDrive, leftB, rightB, gyro):
        '''
        Constructor
        '''
        self.gyro = gyro
        self.max_error = 0.4
        
        self.left = wpilib.CANTalon(leftDrive)
        self.right = wpilib.CANTalon(rightDrive)
        self.left.changeControlMode(wpilib.CANTalon.ControlMode.Voltage)
        self.right.changeControlMode(wpilib.CANTalon.ControlMode.Voltage)
        
        if leftDrive != leftB:
            self.leftB = wpilib.CANTalon(leftB)
            self.rightB = wpilib.CANTalon(rightB)
            self.leftB.changeControlMode(wpilib.CANTalon.ControlMode.Voltage)
            self.rightB.changeControlMode(wpilib.CANTalon.ControlMode.Voltage)
            
        self.setpoint = 0
        
    def stop(self):
        self.arcadeDrive(0,0)
        
        #negative - left
    def pid_rotate(self, angle):
        self.setpoint = angle
        self.integral_accum = 0
        self.gyro.reset()
        
    def pid_calc_error(self):
        return self.setpoint - self.gyro.getAngle()
    
    #GOOD VALUES - 0.03, 0.1 worked with a ~11.8v battery
    #semi good - 0.043, 3, 0.3
    
    def ready_to_shoot(self):
        return abs(self.pid_calc_error()) < self.max_error
    def pid_periodic(self,move):
        #prev 0.023 0.4 0.13
        const_kP = 0.033
        const_kI = 0.5
        const_kFF = 0.17
        error = self.pid_calc_error()
        ##if error < 5:
        #    const_kI = 1.66 - (error / 6)
        self.integral_accum = self.integral_accum + (min(1, max(-1, error)) * 0.005)
        if (self.integral_accum > 0 and error < 0) or (self.integral_accum < 0 and error > 0):
            self.integral_accum = 0
        kP = min(0.4, max(-0.4, const_kP * error))
        kI = const_kI * self.integral_accum
        #kI = kI * kI * 1.0 if kI > 0 else -1.0
        kFF = const_kFF * (1.0 if error > 0 else -1.0)
        SmartDashboard.putNumber("Drive kI", kI)
        SmartDashboard.putNumber("Drive kP", kP)
        SmartDashboard.putNumber("Drive kFF", kFF)
        SmartDashboard.putNumber("Integral Accum", self.integral_accum)
        SmartDashboard.putNumber("Drive Pid Error", error)
        SmartDashboard.putNumber("Drive Pid Setpoint", self.setpoint)
        SmartDashboard.putNumber("Total", -(kP + kI + kFF))
        self.arcadeDrive(move, -(kP + kI + kFF), False, 8)
        
        
    def arcadeDrive(self, move, rotate, squaredInputs=True, voltage=12):
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

        if squaredInputs:
            # square the inputs (while preserving the sign) to increase fine
            # control while permitting full power
            if move >= 0.0:
                move = (move * move)
            else:
                move = -(move * move)
            if rotate >= 0.0:
                rotate = (rotate * rotate)
            else:
                rotate = -(rotate * rotate)

        leftMotorSpeed = 0
        rightMotorSpeed = 0
        
        if move > 0.0:
            if rotate > 0.0:
                leftMotorSpeed = move - rotate
                rightMotorSpeed = max(move, rotate)
            else:
                leftMotorSpeed = max(move, -rotate)
                rightMotorSpeed = move + rotate
        else:
            if rotate > 0.0:
                leftMotorSpeed = -max(-move, rotate)
                rightMotorSpeed = move + rotate
            else:
                leftMotorSpeed = move - rotate
                rightMotorSpeed = -max(-move, -rotate)
        
        self.left.set(leftMotorSpeed * voltage)
        self.right.set(-rightMotorSpeed * voltage)
        
        try:
            self.leftB.set(leftMotorSpeed * voltage)
            self.rightB.set(-rightMotorSpeed * voltage)
        except: pass