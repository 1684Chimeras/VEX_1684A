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
    
    bottom = 0.310
    top = 0.700
    
    bottom_theta = 188
    top_theta = 90


    def __init__(self, left, right, pot ):
        '''
        Constructor
        '''
        self.left = wpilib.VictorSP(left)
        self.right = wpilib.VictorSP(right)
        self.right.setInverted(True)
        
        self.pot = wpilib.AnalogPotentiometer(pot)
        self.last_pos_1 = self.getArmPosition()
        self.last_pos_2 = self.getArmPosition()
        self.last_pos_3 = self.getArmPosition()
        self.last_pos_4 = self.getArmPosition()
        self.last_pos_5 = self.getArmPosition()
        self.setpoint = -1
    
    #got this constant perfect the first time- definitely means she's sayin yes amirite
    #positive constant (negative value) - up
    const_ff = 0.22
    const_p = -0.017
    const_i = 0.01
    const_d = 0.05
    
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
            
    def pid_goto(self, setpoint=-1):
        if(setpoint != -1):
            self.setpoint = setpoint
        if self.setpoint == -1:
            self.setpoint = self.getArmPosition()
            
        kp = self.pid_calc_p(self.setpoint)
        kff = self.pid_calc_ff(self.setpoint)
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

    def set(self, value):
        wpilib.SmartDashboard.putNumber("Potentiometer", self.getArmPosition())
        wpilib.SmartDashboard.putNumber("Potentiometer Raw", self.getPotValue())
        value = max(-0.55, min(0.4, value))
        self.left.set(value)
        self.right.set(value)
        wpilib.SmartDashboard.putNumber("Setpoint", value)
        
    def getPotValue(self):
        return self.pot.get()
    
    def getArmPosition(self):
        pot_value = self.pot.get()
        top = Flipper.top
        bottom = Flipper.bottom
        
        if top > bottom:
            return (pot_value - bottom) / (top - bottom) * (Flipper.top_theta - Flipper.bottom_theta) + Flipper.bottom_theta 
        else:
            return (pot_value - top) / (bottom - top) * (Flipper.bottom_theta - Flipper.top_theta) + Flipper.top_theta 