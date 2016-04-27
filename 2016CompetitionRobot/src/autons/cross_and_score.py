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
        
    def setOuterWorksPosition(self, position):
        self.position = position

    def setOuterWorksType(self, type):
        self.type = type

    def getPIDSetpoint(self):
        print("type {}".format(self.type))
        if self.type == self.OuterWorksType.cheval_de_frise:
            return 160
        
        elif self.type == self.OuterWorksType.guillotine:
            return 170
        
        elif self.type == self.OuterWorksType.ramparts:
            if self.getTimeElapsed() > 3:
                print("Arm DOwn")
                return 205
            else:
                print("Arm Up")
                return 173
        else:
            return 205
    
    def periodic(self):
        #targeting
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
            if self.useGenericRun:
                if not self.driveStage.isFinished():
                    #print("Runnig Drive Stage {}".format(self.getTimeElapsed()))
                    self.driveStage.run()
                elif self.timeoutMark == -1:
                    #print("end drive  Stage {}".format(self.getTimeElapsed()))
                    self.driveStage.terminate()
                    self.timeoutMark = time.time()
                elif self.timeoutMark + 2 < time.time():
                    #print("targeting Drive Stage {}".format(self.getTimeElapsed()))
                    self.targetingEnable = True
                    self.periodic()
                    
            elif self.type == self.OuterWorksType.guillotine or self.type == self.OuterWorksType.cheval_de_frise:
                
                #To begin the auton, drive straight, running the designated intake
                if not self.driveStage.isFinished():
                    
                    #For the cheval auton, you'll want to put the arm down after 1.2 seconds to put the fries down
                    if self.type == self.OuterWorksType.cheval_de_frise:
                        print("type=chvl")
                        if self.getTimeElapsed() < 1.4 + 1.5:
                            print("approach {}".format(self.getTimeElapsed()))
                            self.driveStageZero.run()
                        elif self.getTimeElapsed() < 1.4 + 2.0:
                            print("stop")
                            self.drive_train.arcadeDrive(-0.2,0)
                            self.driveStageZero.terminate()
                        elif self.getTimeElapsed() < 1.4 + 2.5:
                            print("arm down go")
                            print("put arm down")
                            self.flipper.set_override(0.6)
                            self.drive_train.arcadeDrive(0,0)
                        elif not self.driveStage.isFinished():
                            self.flipper.set_override(0.6)
                            self.driveStage.run()
                        else:
                            self.targetingEnable = True
                            self.periodic()
                    else:
                        print("not cheval")
                        if self.getTimeElapsed() > 7.5:
                            self.drive_train.arcadeDrive(0,0)
                            self.flipper.set_override(0)
                        if self.getTimeElapsed() > 6:
                            self.flipper.set_override(0.3)
                            self.drive_train.arcadeDrive(0.8,0)
                        elif not self.driveStage.isFinished():
                            self.driveStage.run()
                        else:
                            self.targetingEnable = True
                            self.periodic()
                    #self.driveStage.run()
                    self.intakeInitialStage.run()
                    
                #Wait for the drive to settle down and the camera to get valid data
                elif self.timeoutMark == -1:
                    #print("Waiting!")
                    self.driveStage.terminate()
                    self.intakeInitialStage.terminate()
                    self.timeoutMark = time.time()
                
                #Shoot
                elif self.timeoutMark + 3 < time.time():
                    self.targetingEnable = True
                    self.periodic()
                    
            elif self.type == self.OuterWorksType.ramparts:
                if self.getTimeElapsed() - 1.4 < 1:
                    self.driveStageZero.run()
                elif self.getTimeElapsed() - 1.4 < 3.5:
                    self.driveStageZero.terminate()
                    self.driveStage.run()
                elif self.getTimeElapsed() - 1.4 < 5:
                    self.driveStage.terminate()
                else:
                    self.targetingEnable = True
                    self.periodic()
            else:
                return
        elif self.getTimeElapsed() > 0.9:
            #print("Arm Down")
            self.flipper.pid_goto(self.getPIDSetpoint())
        else:
            #print("Arm Slam")
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
            self.driveStageZero = drive.DriveRoutine(0.65, 0.1,  timeout=4)
            self.driveStage = drive.DriveRoutine(0.8, 0.1,  timeout=1.2)
            self.intakeInitialStage = run_intake.IntakeRoutine(0,-1)
            self.timeoutMark = -1
        elif self.type == self.OuterWorksType.guillotine:
            self.driveStage = drive.DriveRoutine(0.5, 0.1,  timeout=13)
            self.intakeInitialStage = run_intake.IntakeRoutine(0,1)
            self.timeoutMark = -1
            return
        elif self.type == self.OuterWorksType.moat:
            rammingSpeedTimeout = 3
            self.useGenericRun = True
            #self.bindRight = -0.2
            #self.driveStage = drive.DriveRoutine(self.rammingSpeed, self.bindRight, timeout=self.rammingSpeedTimeout)
        elif self.type == self.OuterWorksType.bump:
            #rammingSpeed = -0.9
            rammingSpeed = 0.8
            rammingSpeedTimeout = 4
            self.driveStageZero = drive.DriveRoutine(0.8, 0.1, timeout=4)
            self.driveStageOne = drive.DriveRoutine(0.8, 0.1, timeout=4)
            self.useGenericRun = False
        elif self.type == self.OuterWorksType.ramparts:
            self.driveStage = drive.DriveRoutine(0.9, 0,  timeout=4.8 , keepTrue=True)
            self.driveStageZero= drive.DriveRoutine(0.6, 0,  timeout=4.8 , keepTrue=True)
        elif self.type == self.OuterWorksType.rough_terrain:
            self.useGenericRun = True
            rammingSpeed = 0.9
            rammingSpeedTimeout = 1.8
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
            self.spinStage = spin.SpinRoutine(40 + indent, timeout=1.5, resetGyro=False)
        elif self.position == self.OuterWorksPosition.rightmost:
            self.spinStage = spin.SpinRoutine(-40 + indent, timeout=1.5, resetGyro=False)
        else:
            self.spinStage = spin.SpinRoutine(0, timeout=1.5, resetGyro=False)
            
        self.targeting = targeting.TargetingRoutine()
        self.autoshoot = auto_shoot.AutomaticShootingRoutine(self.targeting)
        if self.useGenericRun:
            if not hasattr(self, 'driveStage'):
                self.driveStage = drive.DriveRoutine(rammingSpeed, bindRight, timeout=rammingSpeedTimeout)
        
            