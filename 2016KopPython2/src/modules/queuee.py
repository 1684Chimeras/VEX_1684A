'''
Created on Jan 16, 2016

@author: illid_000
'''

import wpilib

class Queue(object):
    '''
    classdocs
    '''



    def __init__(self, params):
        '''
        Constructor
        '''
        self.motor = wpilib.VictorSP(params)
    
    def set(self, value):
        self.motor.set(value)