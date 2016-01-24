'''
Created on Jan 19, 2016

@author: Arhowk
'''

from autons.subroutines._base_subroutine import Subroutine
from autons import cross_and_score, cross_defense, do_nothing, spybot_score

class AutonManager(object):
    '''
    classdocs
    '''
    
    def loadAutons(self):
        self.autons = [cross_and_score.CrossAndScore(), cross_defense.CrossDefense(), do_nothing.DoNothing(), spybot_score.SpybotScore()]
        
    def autonomousInit(self):
        return
    
    def autonomousPeriodic(self):
        return
    

    def __init__(self, climber, driveTrain, flipper, intake, queue, shooter ):
        '''
        Constructor
        '''
        Subroutine.climber = climber
        Subroutine.drive_train = driveTrain
        Subroutine.flipper = flipper
        Subroutine.intake = intake
        Subroutine.queue = queue
        Subroutine.shooter = shooter
        