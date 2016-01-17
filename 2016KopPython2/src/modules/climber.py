'''
Created on Jan 16, 2016

@author: Arhowk
'''
import wpilib

class Climber(object):
    '''
    classdocs
    '''


    def __init__(self, motor):
        '''
        Constructor
        '''
        self.motor = wpilib.VictorSP(motor)
        
    def set(self,value):
        self.motor.set(value)