'''
Created on Feb 13, 2016

@author: illid_000
'''

from autons._base_auton import BaseAutonRoutine

class IntakeRoutine(BaseAutonRoutine):
    '''
    classdocs
    '''


    def __init__(self, speed, timeout=-1):
        '''
        Constructor
        '''
        BaseAutonRoutine.__init__(self)
        self.speed = speed
        if timeout != -1:
            self.setTimeout(timeout)
        
    def periodic(self):
        self.intake.set(self.speed)
        self.queue.set((self.speed  + 0.0) / 1.7)
        
    def onFinished(self):
        self.intake.set(0)