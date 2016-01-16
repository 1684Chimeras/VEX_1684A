'''
Created on Jan 16, 2016

@author: illid_000
'''

import wpilib

class Shooter(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        self.motor = wpilib.CANTalon(params)
    
    def set(self, value):
        self.motor.set(value)