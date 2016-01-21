'''
Created on Jan 19, 2016

@author: Arhowk
'''

from autons.subroutines._base_subroutine import Subroutine

class AutonManager(object):
    '''
    classdocs
    '''
    
    def loadAutons(self):
        return
    
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
        