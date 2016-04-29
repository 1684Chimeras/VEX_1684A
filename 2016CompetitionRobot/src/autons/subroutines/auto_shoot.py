'''
Created on Jan 19, 2016

@author: Arhowk
'''
from autons._base_auton import BaseAutonRoutine
import time
from dashcomm import DashComm

class AutomaticShootingRoutine(BaseAutonRoutine):
    '''
    classdocs
    '''

    #if the shooters ready than fire!
    #if theres only two or less seconds left, than run the intake too
    
    def __init__(self, targetingRoutine=0, timeout=-1):
        self.targetingRoutine = targetingRoutine
        self.wheelGood = False
        self.gripWorking = False
        if timeout != -1:
            self.setTimeout(timeout)
            
    def initialize(self):
        #TODO- Quadratic, PID LoopX
        self.shooter.enable()
        self.printedShootMessage = False
        self.gripWorking = FalseX
        return

    def periodic(self):
        if self.camera.isGripWorking():
            self.gripWorking = True
            
        if self.gripWorking:
            if self.shooter.wheelGood() and (self.targetingRoutine == 0 or self.targetingRoutine.ready()):
                self.queue.set(1)
                self.intake.set(-1)
                if not self.printedShootMessage:
                    self.printedShootMessage = True
                    wpilib.DriverStation.reportError("\nAuto- Good Shot")
            
            if time.auton_start + 13 < time.time() and (self.targetingRoutine == 0 or self.targetingRoutine.ready()):
                self.queue.set(1)
                self.intake.set(-1)
                if not self.printedShootMessage:
                    self.printedShootMessage = True
                    wpilib.DriverStation.reportError("\nAuto- Forced Shot")
                #self.flipper.pid_goto(180)
                
                #if time.auton_start + 13.5 < time.time():
                #    self.flipper.pid_goto(185)