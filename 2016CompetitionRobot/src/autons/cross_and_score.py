import wpilib

from autons.subroutines import drive, shoot, run_intake, targeting, auto_shoot, spin #@UnresolvedImport
import autons._base_auton
import time
class CrossAndScore(autons._base_auton.BaseAutonRoutine):

    def __init__(self, score):
        self.score = score
        autons._base_auton.BaseAutonRoutine.__init__(self)
        self.type = 0
        self.position = 0
        
    class OuterWorksType:
        cheval_de_frise = 0
        drawbridge = 1
        guillotine = 2
        moat = 3
        sally_port = 4
        rough_terrain = 5
        bump = 6
        ramparts = 7

        
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
        
        
    
    def periodic(self):
        if self.getTimeElapsed() > 1.4:
            if self.useGenericRun:
                    if self.driveStage.isFinished():
                        print("Drive Stage DOne: {}".format(self.getTimeElapsed()))
                        if self.timeoutMark == -1:
                            
                            self.timeoutMark = time.time()
                        if self.timeoutMark + 2 < time.time():
                            print("Score Rotuine Begin")
                            if self.score:
                                print("Scoring!")
                                self.flipper.pid_goto(120)
                                self.targeting.run()
                                self.autoshoot.run()
                    else:
                        print("Driving!")
                        self.driveStage.run()
                    return
            elif self.type == self.OuterWorksType.cheval_de_frise or self.type == self.OuterWorksType.guillotine:
                    if self.driveStage.isFinished():
                        self.intakeInitialStage.terminate()
                        if self.timeoutMark == -1:
                            self.timeoutMark = time.time()
                        if self.timeoutMark + 3 < time.time():
                            if self.score:
                                self.flipper.pid_goto(120)
                                self.targeting.run()
                                self.autoshoot.run()
                    else:
                        self.driveStage.run()
                        self.intakeInitialStage.run()
                    return
            else:
                return
        elif self.getTimeElapsed() > 0.9:
            self.flipper.pid_goto(183)
        else:
            self.flipper.set_override(0.6)
    
    def initialize(self, defense, position):
        self._reset()
        self.type = defense
        self.position = position
        self.useGenericRun = False
        self.timeStarted = time.time()
        rammingSpeed = 0.9
        rammingSpeedTimeout = 3
        self.timeoutMark = -1
        bindRight = -0.1
        
        if self.type == self.OuterWorksType.cheval_de_frise:
            self.driveStage = drive.DriveRoutine(0.73, 0.3,  timeout=2.7)
            self.intakeInitialStage = run_intake.IntakeRoutine(0,1)
            self.timeoutMark = -1
            return
        elif self.type == self.OuterWorksType.guillotine:
            self.driveStage = drive.DriveRoutine(0.73, 0.3,  timeout=2.7)
            self.intakeInitialStage = run_intake.IntakeRoutine(0,-1)
            self.timeoutMark = -1
            return
        elif self.type == self.OuterWorksType.moat:
            rammingSpeedTimeout = 0.83 #actual value 1.4
            self.useGenericRun = True
            #self.bindRight = -0.2
            #self.driveStage = drive.DriveRoutine(self.rammingSpeed, self.bindRight, timeout=self.rammingSpeedTimeout)
        elif self.type == self.OuterWorksType.bump:
            self.useGenericRun = True
            #self.driveStage = drive.DriveRoutine(self.rammingSpeed, self.bindRight, timeout=self.rammingSpeedTimeout)
        elif self.type == self.OuterWorksType.drawbridge:
            self.useGenericRun = True
        elif self.type == self.OuterWorksType.guillotine:
            self.useGenericRun = True
        elif self.type == self.OuterWorksType.ramparts:
            self.useGenericRun = True
        elif self.type == self.OuterWorksType.rough_terrain:
            self.useGenericRun = True
        elif self.type == self.OuterWorksType.sally_port:
            self.useGenericRun = True
            
        self.targeting = targeting.TargetingRoutine()
        self.autoshoot = auto_shoot.AutomaticShootingRoutine(self.targeting)
        if self.useGenericRun:
            if not hasattr(self, 'driveStage'):
                self.driveStage = drive.DriveRoutine(rammingSpeed, bindRight, timeout=rammingSpeedTimeout)
        
            