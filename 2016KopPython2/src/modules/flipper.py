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
    
    bottom = 0.161
    top = 0.668
    
    bottom_theta = 190
    top_theta = 75


    def __init__(self, left, right, pot ):
        '''
        Constructor
        '''
        self.left = wpilib.VictorSP(left)
        self.right = wpilib.VictorSP(right)
        self.right.setInverted(True)
        
        self.pot = wpilib.AnalogPotentiometer(pot)
    
    #got this constant perfect the first time- definitely means she's sayin yes amirite
    #positive constant (negative value) - up
    const_sin = 0.15
    
    def pid_calc_ff(self):
        return Flipper.const_sin * math.cos(self.getArmPosition() * (3.14 / 180.0))
    
    def pid_stay(self):
        #print("angle {} pid {} error {}".format(self.getArmPosition(), self.pid_calc_ff(), math.cos(self.getArmPosition() * (3.14 / 180.0))))
        #print(self.pid_calc_ff())
        self.set(self.pid_calc_ff())
        
    def set(self, value):
        self.left.set(value)
        self.right.set(value)
        
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