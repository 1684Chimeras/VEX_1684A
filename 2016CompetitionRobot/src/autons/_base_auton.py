'''
Created on Jan 19, 2016

@author: Arhowk
'''

import time

class BaseAutonRoutine(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.terminated = False
        self.initialized = False
        self.timeout = 9999
        self.wasFinished = False
        
    def initialize(self):
        return
    
    
    def start(self):
        self.timeStarted = time.time()
        self.initialized = True
        self.terminated = False 
        self.wasFinished = False
        self.initialize()
    
    def periodic(self):
        return
    
    def isFinished(self):
        if not self.initialized:
            return False
        
        b =  self.isTimedOut() or self.terminated
        if b and not self.wasFinished:
            self.onFinished()
            self.wasFinished = True
        return b
    
    def getTimeElapsed(self):
        return time.time() - self.timeStarted 
    
    def getTimeRemaining(self):
        return self.timeStarted + self.timeout - time.time()
    
    def isTimedOut(self):
        return self.timeStarted + self.timeout < time.time()
    
    def setTimeout(self, timeout):
        self.timeout = timeout
        self.timeStarted = time.time()
        
    def terminate(self):
        if not self.wasFinished:
            self.wasFinished = True
            self.onFinished()
        self.terminated = True
        
    def restart(self):
        self.initialized = False
        self.terminated = False
        self.wasFinished = False
        
    def onFinished(self):
        return
        
    def run(self):
        if not self.isFinished():
            if not self.initialized:
                self.initialized = True
                self._initialize()
            self.periodic()