'''
Created on Jan 16, 2016

@author: Arhowk
'''
import wpilib

class Climber(object):
    '''
    classdocs
    '''


    def __init__(self, pulley, tape):
        '''
        Constructor
        '''
        self.pulley = wpilib.CANTalon(pulley)
        self.tape = wpilib.VictorSP(tape)
        
    def setPulley(self,value):
        self.pulley.set(value)
        
    def setTape(self, value):
        if(value < 0):
            self.tape.set(value )
        else:
            self.tape.set(value * 0.5)