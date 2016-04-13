'''
Created on Jan 19, 2016

@author: Arhowk
'''
from autons._base_auton import BaseAutonRoutine

class DriveRoutine(BaseAutonRoutine):
    '''
    classdocs
    '''


    def __init__(self, move=0, rotate=0, distance=0, timeout=-1, keepTrue=False):
        self.move = move
        self.rotate = rotate
        self.distance = distance
        self.keepTrue = keepTrue
        if timeout != -1:
            self.setTimeout(timeout)
            
    def initalize(self):
        #TODO- Quadratic, PID Loop
        BaseAutonRoutine._reset(self)
        if self.keepTrue:
            self.driveTrain.pid_rotate(0)
        else:
            self.drive_train.arcadeDrive(self.move, self.rotate)
        

    def periodic(self):
        if self.keepTrue:
            self.driveTrain.pid_periodic(self.move)
        else:
            self.drive_train.arcadeDrive(self.move, self.rotate)
    
    def onFinished(self):
        self.drive_train.arcadeDrive(0,0)