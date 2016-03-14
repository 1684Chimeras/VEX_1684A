import wpilib

from autons.subroutines import drive, run_intake, targeting, auto_shoot, spin #@UnresolvedImport
import autons._base_auton
import time
from dashcomm import DashComm
from pip._vendor.distlib._backport.tarfile import TUREAD

class CrossAndScore(autons._base_auton.BaseAutonRoutine):

    def __init__(self, score):
        autons._base_auton.BaseAutonRoutine.__init__(self)

        self.score = score        
        self.type = 0
        self.position = 0
        
    class OuterWorksType:
        cheval_de_frise = 1
        drawbridge = 2
        guillotine = 3
        moat = 4
        sally_port = 5
        rough_terrain = 6
        bump = 7
        ramparts = 8

        
    class OuterWorksPosition:
        leftmost = 1
        left = 2
        middle = 3
        right = 4
        rightmost = 5
        
    def positionToString(self, position):        
        return "undefined"
    
    def typeToString(self, type):
        return "undefined"
    
    def setOuterWorksPosition(self, position):
        self.position = position

    def setOuterWorksType(self, type):
        self.type = type

    def getPriority(self):
        return 1

    def getName(self):
        return "Cross Goal And Score"

    def getDescription(self):
        return "Attempts to cross the goal and score.\r\n\r\nCurrent Position: " + self.positionToString(self.position) + "\r\nCurrent Defense Type: " + self.typeToString(self.type)
        
    def getPIDSetpoint(self):
        if self.type == self.OuterWorksType.cheval_de_frise:
            return 180
        elif self.type == self.OuterWorksType.guillotine:
            return 170
        else:
            return 205
    
    def periodic(self):
        if self.targetingEnable:
            if self.score:
                self.flipper.pid_goto(120)
                if hasattr(self, "spinStage"):
                    if self.spinStage.isFinished():
                        self.spinStage.terminate()
                        self.targeting.run()
                        self.autoshoot.run()
                    else:
                        self.spinStage.run()
                else:
                    self.targeting.run()
                    self.autoshoot.run()
        elif self.getTimeElapsed() > 1.4:
            self.flipper.pid_goto(self.getPIDSetpoint())
            #print("HELLO {}".format(self.type))
            if self.useGenericRun:
                #print("Drive Stage")
                if not self.driveStage.isFinished():
                    print("Driving!")
                    self.driveStage.run()
                elif self.timeoutMark == -1:
                    print("Waiiting")
                    self.driveStage.terminate()
                    self.timeoutMark = time.time()
                elif self.timeoutMark + 2 < time.time():
                    print("Shooting")
                    self.targetingEnable = True
                    self.periodic()
            elif self.type == self.OuterWorksType.cheval_de_frise or self.type == self.OuterWorksType.guillotine:
                print("Cheval de Frise Periodic")
                if not self.driveStage.isFinished():
                    #print("Driving!")
                    if self.getTimeElapsed() > 1.8 and self.type == self.OuterWorksType.cheval_de_frise:
                        self.flipper.set_override(0.6)
                        
                    self.driveStage.run()
                    self.intakeInitialStage.run()
                    
                elif self.timeoutMark == -1:
                    #print("Waiting!")
                    self.driveStage.terminate()
                    self.intakeInitialStage.terminate()
                    self.timeoutMark = time.time()
                elif self.timeoutMark + 3 < time.time():
                    #print("Scoring!")
                    #if self.score:
                    #    self.flipper.pid_goto(120)
                    #    self.targeting.run()
                    #    self.autoshoot.run()
                    self.targetingEnable = True
                    self.periodic()
            else:
                return
        elif self.getTimeElapsed() > 0.9:
            print("moving ram down")
            self.flipper.pid_goto(self.getPIDSetpoint())
        else:
            print("override falling")
            self.flipper.set_override(0.6)
    
    def initialize(self):
        self.useGenericRun = False
        self.timeStarted = time.time()
        self.targetingEnable = False
        rammingSpeed = 0.9
        rammingSpeedTimeout = 3
        self.timeoutMark = -1
        bindRight = -0.1
        
        if self.type == self.OuterWorksType.cheval_de_frise:
            self.driveStage = drive.DriveRoutine(0.8, 0.3,  timeout=2.7)
            self.intakeInitialStage = run_intake.IntakeRoutine(0,-1)
            self.timeoutMark = -1
        elif self.type == self.OuterWorksType.guillotine:
            self.driveStage = drive.DriveRoutine(0.7, 0.1,  timeout=3.4)
            self.intakeInitialStage = run_intake.IntakeRoutine(0,1)
            self.timeoutMark = -1
            return
        elif self.type == self.OuterWorksType.moat:
            rammingSpeedTimeout = 1.4
            self.useGenericRun = True
            #self.bindRight = -0.2
            #self.driveStage = drive.DriveRoutine(self.rammingSpeed, self.bindRight, timeout=self.rammingSpeedTimeout)
        elif self.type == self.OuterWorksType.bump:
            #rammingSpeed = -0.9
            self.useGenericRun = True
        elif self.type == self.OuterWorksType.ramparts:
            self.useGenericRun = True
        elif self.type == self.OuterWorksType.rough_terrain:
            self.useGenericRun = True
            rammingSpeed = 0.9
            rammingSpeedTimeout = 4
        elif self.type == self.OuterWorksType.sally_port: #sally port is actually just a testing ground for low bar
            rammingSpeedTimeout = 0.83 #actual value 1.4
            self.useGenericRun = True
        elif self.type == self.OuterWorksType.drawbridge:
            rammingSpeedTimeout = 0.4
            rammingSpeed = 0.7
            self.useGenericRun = True
        
        indent = 0
        if self.type == self.OuterWorksType.bump:
            indent = 180
        if self.position == self.OuterWorksPosition.left:
            self.spinStage = spin.SpinRoutine(40 + indent, timeout=1)
        elif self.position == self.OuterWorksPosition.rightmost:
            self.spinStage = spin.SpinRoutine(-40 + indent, timeout=1)
            
        self.targeting = targeting.TargetingRoutine()
        self.autoshoot = auto_shoot.AutomaticShootingRoutine(self.targeting)
        if self.useGenericRun:
            if not hasattr(self, 'driveStage'):
                self.driveStage = drive.DriveRoutine(rammingSpeed, bindRight, timeout=rammingSpeedTimeout)
        
            