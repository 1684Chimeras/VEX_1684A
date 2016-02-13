'''
Created on Jan 19, 2016

@author: Arhowk
'''
from autons._base_auton import BaseAutonRoutine

class TargetingRoutine(BaseAutonRoutine):
    '''
    classdocs
    '''


    def __init__(self, timeout=-1):
        '''
        Constructor
        '''
        BaseAutonRoutine.__init__(self)
        if timeout != -1:
            self.setTimeout(timeout)
            
    def ready(self):
        return self.drive_train.ready_to_shoot() and self.getTimeElapsed() > 2.5
    
    def initialize(self):
        #TODO- Quadratic, PID Loop
        self.drive_train.pid_rotate(self.camera.getRotationOffset())

    def periodic(self):
        self.drive_train.pid_periodic(0)