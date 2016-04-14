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
            
    def initialize(self):
        #TODO- Quadratic, PID Loop
        #BaseAutonRoutine._reset(self)
        #print("init")
        if self.keepTrue:
            #print("Initialize Rotate")
            self.drive_train.pid_rotate(0)
        else:
            #print("Initialize Periodic")
            self.drive_train.arcadeDrive(self.move, self.rotate)
        

    def periodic(self):
        #print("Periodic")
        if self.keepTrue:
            #print("Periodic kt")
            self.drive_train.pid_periodic(self.move)
        else:
            #print("Periodic b")
            self.drive_train.arcadeDrive(self.move, self.rotate)
    
    def onFinished(self):
        self.drive_train.arcadeDrive(0,0)