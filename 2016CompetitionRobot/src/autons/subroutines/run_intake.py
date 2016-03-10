'''
Created on Feb 13, 2016

@author: illid_000
'''

from autons._base_auton import BaseAutonRoutine

class IntakeRoutine(BaseAutonRoutine):
    '''
    classdocs
    '''


    def __init__(self, speed, speedOut=-123, timeout=-1):
        self.speed = speed
        if speedOut == -123:
            self.speedOut = self.speed
        else:
            self.speedOut = speedOut
        if timeout != -1:
            self.setTimeout(timeout)
        
    def periodic(self):
        self.intake.set(self.speed, self.speedOut)
        self.queue.set((self.speed  + 0.0) / 1.7)
        
    def onFinished(self):
        self.intake.set(0)
        self.queue.set(0)