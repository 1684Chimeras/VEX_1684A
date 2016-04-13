import wpilib 
import autons._base_auton

class DoNothing(autons._base_auton.BaseAutonRoutine):

    def getPriority(self):
        return 0

    def getName(self):
        return "Do Nothing"

    def getDescription(self):
        return "Does nothing, what do you want with me?"
        
    def periodic(self):
        print("do nothing")
        return
    
    def initialize(self):
        print("initialize do nothing")
        return