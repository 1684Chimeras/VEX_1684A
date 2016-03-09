'''
Created on Jan 19, 2016

@author: Arhowk
'''
from autons._base_auton import BaseAutonRoutine
import time

class AutomaticShootingRoutine(BaseAutonRoutine):
    '''
    classdocs
    '''

    #if the shooters ready than fire!
    #if theres only two or less seconds left, than run the intake too
    
    def __init__(self, targetingRoutine=0, timeout=-1):
        '''
        Constructor
        '''
        
        BaseAutonRoutine.__init__(self)
        self.targetingRoutine = targetingRoutine
        self.wheelGood = False
        if timeout != -1:
            self.setTimeout(timeout)
            
    def initialize(self):
        #TODO- Quadratic, PID Loop
        BaseAutonRoutine._reset(self)
        print("Set PDI")
        self.shooter.enable()
        print("Set pid done")
        return

    def periodic(self):
        if self.shooter.wheelGood():
            self.wheelGood = True
        spunQueue = False
        spunIntake = False
        if self.wheelGood:
            if self.targetingRoutine != 0:
                if self.targetingRoutine.ready():
                    self.queue.set(1)
                    self.intake.set(-1)
                    self.spunQueue = True
        
        if time.auton_start + 8 < time.time():
            spunQueue = True
            self.queue.set(1)
            self.intake.set(-1)
            self.flipper.pid_goto(180)
            
            if time.auton_start + 9.5 < time.time():
                self.spunIntake = True
                self.intake.set(-1)
            self.flipper.pid_goto(185)