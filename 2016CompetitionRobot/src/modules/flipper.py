'''
Created on Jan 16, 2016

@author: illid_000
'''
import wpilib
import math

class Flipper(object):
    '''
    classdocs
    '''
    
    bottom = 270
    top = 3430
    throw = 3780 - 662
    
    bottom_theta = 187.5
    top_theta = 90


    def __init__(self, left, right, pot ):
        '''
        Constructor
        '''
        self.left = wpilib.CANTalon(left)
        self.right = wpilib.CANTalon(right)
    
        self.left.changeControlMode(wpilib.CANTalon.ControlMode.Voltage)
        self.right.changeControlMode(wpilib.CANTalon.ControlMode.Voltage)
    
        #self.right.reverseOutput(True)
        self.talonEncoder = self.left
        self.talonEncoder.setFeedbackDevice(7)
        #self.right.configEncoderCodesPerRev(4096)
         
        self.last_pos_1 = self.getArmPosition()
        self.last_pos_2 = self.getArmPosition()
        self.last_pos_3 = self.getArmPosition()
        self.last_pos_4 = self.getArmPosition()
        self.last_pos_5 = self.getArmPosition()
        self.setpoint = -1
    
    def pid_calc_ff(self, pos=-1):
        if(pos == -1):
            pos = self.getArmPosition()
        return Flipper.const_ff * math.cos(pos * (3.14 / 180.0))
    
    def pid_calc_p(self, pos=-1):
        if(pos == -1):
            return 0
        return Flipper.const_p * (self.getArmPosition() - pos)
    
    def pid_calc_i(self, pos=-1):
        if(pos == -1):
            return self.i_accum
        if(pos != self.i_accum_last_pos):
            self.i_accum_last_pos = pos
            self.i_accum = 0
        return 0
    
    def pid_calc_d(self, pos=-1):
        last_pos_5 = self.last_pos_5
        self.last_pos_5 = self.last_pos_4
        self.last_pos_4 = self.last_pos_3
        self.last_pos_3 = self.last_pos_2
        self.last_pos_2 = self.last_pos_1
        self.last_pos_1 = self.getArmPosition()
        
        self.lastPos = self.getArmPosition()
        
        return self.const_d * (((last_pos_5 + self.last_pos_3) / 2) - ((self.last_pos_1 + self.last_pos_3) / 2))
        
    def pid_stay(self):
        #print("angle {} pid {} error {}".format(self.getArmPosition(), self.pid_calc_ff(), math.cos(self.getArmPosition() * (3.14 / 180.0))))
        #print(self.pid_calc_ff())
        self.set(self.pid_calc_ff())
        
    def pid_lock(self):
        self.pid_goto(self.getArmPosition())
            
    #positive constant (negative value) - up
    #previous before drivers meeting - 0.26 ff, -0.017[
    const_ff = 0.34
    const_p = -0.021
    const_i = 0.01
    const_d = 0.02
    
    def pid_goto(self, setpoint=-1):
        if(setpoint != -1):
            self.setpoint = setpoint
        if self.setpoint == -1:
            self.setpoint = self.getArmPosition()
            
        if self.setpoint > 190:
            #print("Set Comp Rate {}".format(0.1))
            self.left.setVoltageRampRate(1.2)
            self.right.setVoltageRampRate(1.2)
        else:
            #print("Set Comp Rate {}".format(500))
            self.left.setVoltageRampRate(500)
            self.right.setVoltageRampRate(500)
            
        kp = self.pid_calc_p(self.setpoint)
        kff = self.pid_calc_ff(self.getArmPosition())
        kd = self.pid_calc_d(self.setpoint)
        
        wpilib.SmartDashboard.putNumber("kP", kp)
        wpilib.SmartDashboard.putNumber("kD", kd)
        wpilib.SmartDashboard.putNumber("kFF", kff)
        
        if(self.setpoint > 184 and self.getArmPosition() > 184):
            wpilib.SmartDashboard.putBoolean("No Power", True)
            self.set(0)
        else:
            wpilib.SmartDashboard.putBoolean("No Power", True)
            self.set(kp + kff + kd)

    def set_override(self, value):
        wpilib.SmartDashboard.putNumber("Potentiometer", self.getArmPosition())
        wpilib.SmartDashboard.putNumber("Potentiometer Raw", self.getPotValue())
        #value = max(-0.55, min(0.4, value))
        self.left.setVoltageRampRate(5000)
        self.right.setVoltageRampRate(5000)
        if(value > 1 and self.getArmPosition() > 185):
            value = 0
        self.left.set(value * 7)
        self.right.set(-value * 7)
        wpilib.SmartDashboard.putNumber("Setpoint", value)
        
    def driver_control(self, value):
        self.set(value + self.pid_calc_ff(self.getArmPosition()))
        
    def set(self, value):
        wpilib.SmartDashboard.putNumber("Potentiometer", self.getArmPosition())
        wpilib.SmartDashboard.putNumber("Potentiometer Raw", self.getPotValue())
        self.left.setVoltageRampRate(5000)
        self.right.setVoltageRampRate(5000)
        if self.getArmPosition() < 100:
            value = max(-0.9, min(0.9, value))
        else:
            value = max(-0.7, min(0.4, value))
        if(value > 1 and self.getArmPosition() > 185):
            value = 0
        self.left.set(value * 7)
        self.right.set(-value * 7)
        wpilib.SmartDashboard.putNumber("Setpoint", value)
        
    def getPotValue(self):
        return self.talonEncoder.getPulseWidthPosition()
        #return self.pot.get()
    
    def getArmPosition(self):
        pot_value = self.getPotValue()
        top = Flipper.top
        bottom = Flipper.bottom
        
        if top > bottom:
            return (pot_value - bottom) / (top - bottom) * (Flipper.top_theta - Flipper.bottom_theta) + Flipper.bottom_theta 
        else:
            return (pot_value - top) / (bottom - top) * (Flipper.bottom_theta - Flipper.top_theta) + Flipper.top_theta 