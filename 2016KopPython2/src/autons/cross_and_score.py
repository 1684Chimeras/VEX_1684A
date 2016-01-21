import wpilib
import _base_auton 

from subroutines import drive, shoot, spin #@UnresolvedImport

class CrossAndScore(_base_auton.BaseAutonRoutine):

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
        return
    
    def initialize(self):
        return