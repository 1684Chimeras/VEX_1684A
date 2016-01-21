import wpilib
import time
 

class Subroutine:
    
    def __init__(self):
        self.timeoutDur == -1
        self.timeoutStart = 0
        self.finished = False
    
    def setTimeout(self, dur):
        self.timeoutDur = dur
        self.timeoutStart = time.time()
    
    def finish(self):
        self.finished = True
        
    def isFinished(self):
        return self.finished or (self.timeout != -1 and self.timeoutStart + self.timeoutDur < time.time())
    
    def queueNext(self, nextSubroutine):
        return
    
    def execute(self):
        if self.isFinished():
            if self.queue:
                