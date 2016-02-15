'''
Created on Jan 19, 2016

@author: Arhowk
'''
from autons._base_auton import BaseAutonRoutine

class DriveRoutine(BaseAutonRoutine):
    '''
    classdocs
    '''


    def __init__(self, move=0, rotate=0, distance=0, timeout=-1):
        '''
        Constructor
        '''
        BaseAutonRoutine.__init__(self)
        self.move = move
        self.rotate = rotate
        self.distance = distance
        if timeout != -1:
            self.setTimeout(timeout)
            
    def initalize(self):
        #TODO- Quadratic, PID Loop
        self.drive_train.arcadeDrive(self.move, self.rotate)
        
        return

    def periodic(self):
        self.drive_train.arcadeDrive(self.move, self.rotate)
        return
    
    def onFinished(self):
        self.drive_train.arcadeDrive(0,0)
        return