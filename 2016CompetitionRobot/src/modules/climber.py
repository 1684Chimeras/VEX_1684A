'''
Created on Jan 16, 2016

@author: Arhowk
'''
import wpilib

class Climber(object):
    '''
    classdocs
    '''

    min = 0.0
    max = 4096.0
    angle_min = 0
    throw = 180.0

    def __init__(self, pulley, tape):
        '''
        Constructor
        '''
        self.pulley = wpilib.CANTalon(pulley)
        self.tape = wpilib.VictorSP(tape)
        
        self.encoderMotor = self.pulley
        self.encoderMotor.setFeedbackDevice(7)
        
    def getHookPosition(self):
        return self.angle_min + (1 - (self.max - self.getHookEncoder()) / (self.max - self.min)) * self.throw
    
    def getHookEncoder(self):
        return self.encoderMotor.getPulseWidthPosition()    
    
    def setPulley(self,value):
        self.pulley.set(value)
        
    def setTape(self, value):
        if(value < 0):
            self.tape.set(value )
        else:
            self.tape.set(value * 0.5)