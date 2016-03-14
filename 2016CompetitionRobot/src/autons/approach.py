import wpilib
import autons._base_auton
import time
from autons.subroutines import drive

class Approach(autons._base_auton.BaseAutonRoutine):
    def __init__(self):
        autons._base_auton.BaseAutonRoutine.__init__(self)
        self.timeStarted = time.time()
        
        self.driveStage1= drive.DriveRoutine(0.7, 0, timeout=444)
        self.driveStage2= drive.DriveRoutine(0, 0, timeout=444)
    def getPriority(self):
        return

    def getName(self): 
        return

    def getDescription(self):
        return
        
    def periodic(self):
        #print("Periodic!")
        if self.getTimeElapsed() < 0.9:
            #print("1! {}".format(self.getTimeElapsed()))
            self.flipper.set_override(0.6)
        elif self.getTimeElapsed() < 1.4:
            self.flipper.pid_goto(205)
        elif self.getTimeElapsed() < 2.4:
            self.driveStage1.periodic()
        else:
            #print("2: {}".format(self.getTimeElapsed()))
            self.driveStage2.periodic()
        return
    
    def initialize(self):
        self.timeStarted = time.time()
        return
    