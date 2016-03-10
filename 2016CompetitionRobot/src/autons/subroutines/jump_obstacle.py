'''
Created on Jan 20, 2016

Jumps an obstacl, assuming that the back robot of the bumper is touching the line

@author: Arhowk
'''
import _base_subroutine

class JumpObstacle(_base_subroutine.Subroutine):
    '''
    classdocs
    '''
    
    class OuterWorksType:
        cheval_de_frise = 0
        drawbridge = 1
        guillotine = 2
        moat = 3
        sally_port = 4
        rough_terrain = 5
        bump = 6
        ramparts = 7
        
    
    def mate(self, otherRoutine):
        return
    
    def initialize(self):
        return
    
    def periodicRun(self):
        speed = min(self.getTimeElapsed() * 4 + 0.5, 1)
        
        return
    
    def periodic(self):
        return
    
        
    def __init__(self, defenseType):
        self.type = defenseType
        types = self.OuterWorksType
        if defenseType == self.OuterWorksType.moat or defenseType == self.OuterWorksType.rough_terrain or defenseType == self.OuterWorksType.bump:
            self.func = self.periodicRun
            if defenseType == types.moat:
                self.time = 2
            elif defenseType == types.bump:
                self.time = 2
            elif defenseType == types.rough_terrain:
                self.time = 2
            self.setTimeout(self.time)
            
            