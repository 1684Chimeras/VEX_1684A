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
        self.deg = deg
    
    def initialize(self):
        self.drive.pid_rotate(self.deg)
        
    def periodic(self):
        self.drive.pid_periodic()
        
    def onFinished(self):
        self.drive.stop()