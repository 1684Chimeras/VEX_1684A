import wpilib 
import _base_auton

class DoNothing(_base_auton.BaseAutonRoutine):

    def getPriority(self):
        return 0

    def getName(self):
        return "Do Nothing"

    def getDescription(self):
        return "Does nothing, what do you want with me?"
        
    def periodic(self):
        return
    
    def initialize(self):
        return