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
        if leftDrive == leftB:
            self.robotDrive = wpilib.RobotDrive(leftDrive, rightDrive)
        else:
            self.robotDrive = wpilib.RobotDrive(leftDrive, leftB, rightDrive, rightB)
        self.setpoint = 0
        #self.robotDrive.setInvertedMotor(wpilib.RobotDrive.MotorType.kFrontLeft, True)
        #self.robotDrive.setInvertedMotor(wpilib.RobotDrive.MotorType.kRearRight, True)
        
    def pid_rotate(self, angle):
        print("ROtate to angle {}".format(angle))
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
        const_kP = 0.023
        const_kI = 0.6
        const_kFF = 0.29
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
        self.arcadeDrive(move, -(kP + kI + kFF))
        
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