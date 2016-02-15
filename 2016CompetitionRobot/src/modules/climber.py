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
        self.pulley = wpilib.VictorSP(pulley)
        self.tape = wpilib.VictorSP(tape)
        
    def setPulley(self,value):
        self.pulley.set(value)
        
    def setTape(self, value):
        self.tape.set(value)