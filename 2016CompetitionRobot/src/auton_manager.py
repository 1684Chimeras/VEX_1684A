'''
Created on Jan 19, 2016

@author: Arhowk
'''

from autons.subroutines._base_subroutine import Subroutine
from autons._base_auton import BaseAutonRoutine
from autons import cross_and_score, cross_defense, do_nothing, spybot_score, approach
import time

class AutonManager(object):
    '''
    classdocs
    '''
    
    def loadAutons(self):
        self.autons = [ do_nothing.DoNothing(),cross_and_score.CrossAndScore(), cross_defense.CrossDefense(), spybot_score.SpybotScore(), approach.Approach()]
        
    def autonomousInit(self, mode, defense, position):
        self.selectedAuton = self.autons[mode]
        self.selectedAuton.initialize(defense,position)
    
    def autonomousPeriodic(self):
        self.selectedAuton.periodic()
        
    def lightRoutineCustom(self, left, right, routine=12345):
        if(routine == 12345):
            routine = self.LEDPattern
        
        if not self.LEDWasStarted or time.time() - self.lastLEDTime > 1:
            self.LEDWasStarted = True
            self.lastLEDTime = time.time()
            self.lastLEDState = 0
        
        if time.time() - self.lastLEDTime > self.LEDTimingPeriod:
            self.lastLEDState = self.lastLEDState + 1
            
            if self.lastLEDState > len(routine) / 2:
                self.lastLEDState = 0
            self.lastLEDTime = time.time()
        
            left.set(self.LEDPattern[self.lastLEDState*2:self.lastLEDState*2+1] == "1")
            right.set(self.LEDPattern[self.lastLEDState*2+1:self.lastLEDState*2+2] == "1")
            
    def lightRoutine(self, left, right, type=0):
        if type == "Auto":
            self.lightRoutineCustom(left, right, self.AutoLEDPattern)
            return
        elif type == "Climb":
            self.lightRoutineCustom(left, right, self.ClimbLEDPattern)
            return
        #two sets of both on/off - 1/4sec period
        #three sets of seperate on/off - 1/7sec period
        #both on- 1sec period
        #both off - 0.75sec period
        if self.lastLEDState <= 3:
            if time.time() - self.lastLEDTime > 1.0/4.0:
                self.lastLEDState = self.lastLEDState + 1
                self.lastLEDTime = time.time()
                self.lastLEDFlicker = not self.lastLEDFlicker
                left.set(not self.lastLEDFlicker)
                right.set(not self.lastLEDFlicker)
            elif self.lastLEDState == 0:
                self.lastLEDFlicker = True
                left.set(True)
                right.set(True)
        elif self.lastLEDState <= 11:
            if time.time() - self.lastLEDTime > 1.0/10.0:
                self.lastLEDState = self.lastLEDState + 1
                self.lastLEDTime = time.time()
                self.lastLEDFlicker = not self.lastLEDFlicker
                left.set(self.lastLEDFlicker)
                right.set(not self.lastLEDFlicker)
            elif self.lastLEDState == 4:
                self.lastLEDFlicker = False
                left.set(self.lastLEDFlicker)
                right.set(not self.lastLEDFlicker)
        elif self.lastLEDState == 12:
            if time.time() - self.lastLEDTime > 1:
                self.lastLEDState = self.lastLEDState + 1
                self.lastLEDTime = time.time()
            else:
                left.set(True)
                right.set(True)
        elif self.lastLEDState == 13:
            if time.time() - self.lastLEDTime > 1:
                self.lastLEDState = 0
                self.lastLEDTime = time.time()
            else:
                left.set(False)
                right.set(False)
        
        

    def __init__(self, climber, driveTrain, flipper, intake, queue, shooter, camera):
        '''
        Constructor
        '''
        #60hz
        #Dormant
        self.ClimbLEDPattern = (("11" * int(20)) + ("00" * int(20))) * 2 + (("10" * int(9)) + ("01" * int(9))) * 5 + ("11" * 60) + ("00" * 60)
        
        #Sinusoidal
        self.AutoLEDPattern = ""
        for i in range(1,6):
            self.AutoLEDPattern = self.AutoLEDPattern + "11" * i + "00" * i
        for i in range(1,6):
            self.AutoLEDPattern = self.AutoLEDPattern + "11" * (6-i) + "00" * (6-i)
        
        self.LEDTimingPeriod = 0.001
        self.LEDWasStarted = False
        self.lastLEDTime = 0
        self.lastLEDState = 0
        self.lastLEDFlicker = False
        self.loadAutons()
        self.selectedAuton = self.autons[0]
        Subroutine.climber = climber
        Subroutine.drive_train = driveTrain
        Subroutine.flipper = flipper
        Subroutine.intake = intake
        Subroutine.queue = queue
        Subroutine.shooter = shooter
        
        BaseAutonRoutine.climber = climber
        BaseAutonRoutine.drive_train = driveTrain
        BaseAutonRoutine.flipper = flipper
        BaseAutonRoutine.intake = intake
        BaseAutonRoutine.queue = queue
        BaseAutonRoutine.shooter = shooter
        BaseAutonRoutine.camera = camera
        