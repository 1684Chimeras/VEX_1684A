'''
Created on Jan 19, 2016

@author: Arhowk
'''

from autons._base_auton import BaseAutonRoutine

class SpinRoutine(BaseAutonRoutine):
    '''
    classdocs
    '''


    def __init__(self, deg):
        '''
        Constructor
        '''
        BaseAutonRoutine.__init__(self)
        self.deg = deg
    
    def initialize(self):
        BaseAutonRoutine._initialize(self)
        BaseAutonRoutine._reset(self)
        
        self.drive.pid_rotate(self.deg)
        
    def periodic(self):
        self.drive.pid_periodic()