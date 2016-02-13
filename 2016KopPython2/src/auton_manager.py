'''
Created on Jan 19, 2016

@author: Arhowk
'''

from autons.subroutines._base_subroutine import Subroutine
from autons._base_auton import BaseAutonRoutine
from autons import cross_and_score, cross_defense, do_nothing, spybot_score

class AutonManager(object):
    '''
    classdocs
    '''
    
    def loadAutons(self):
        self.autons = [ do_nothing.DoNothing(),cross_and_score.CrossAndScore(), cross_defense.CrossDefense(), spybot_score.SpybotScore()]
        
    def autonomousInit(self, mode, defense, position):
        self.selectedAuton = self.autons[mode]
        self.selectedAuton.initialize(defense,position)
    
    def autonomousPeriodic(self):
        self.selectedAuton.periodic()
    

    def __init__(self, climber, driveTrain, flipper, intake, queue, shooter, camera):
        '''
        Constructor
        '''
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
        