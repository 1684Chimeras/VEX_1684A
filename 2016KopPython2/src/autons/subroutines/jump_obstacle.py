'''
Created on Jan 20, 2016

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
    
    def periodic(self):
        return
    
        
    def __init__(self, defenseType):
        '''
        Constructor
        '''
        self.type = defenseType