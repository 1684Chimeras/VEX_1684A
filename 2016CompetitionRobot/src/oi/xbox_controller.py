'''
Created on Jan 25, 2016

@author: Arhowk
'''
from types import IntType

import wpilib

class XboxController(object):
    '''
    classdocs
    '''
    
    class Bindings:
        a=1
        b=2
        x=3
        y=4
        
    class WirelessPs4Module:
        def getRawAxis(self, axis):
            if axis == 4:
                axis = 2
            elif axis == 2:
                return (self.joy.getRawAxis(3) + 1) / 2
            elif axis == 3:
                return (self.joy.getRawAxis(4) + 1) / 2
            return self.joy.getRawAxis(axis)
        
        def getRawButton(self, button):
            if button == 1:
                button = 2
            elif button == 2:
                button = 3
            elif button == 3:
                button = 1
            elif button == 9:
                button = 7
            elif button == 10:
                button = 8
            elif button == 11:
                button = 9
            elif button == 12:
                button = 10
        
            return self.joy.getRawButton(button)
        
        def getPOV(self):
            return self.joy.getPOV()
        
        def __init__(self, joy):
            self.joy = joy #down in my heart
        
    class NormalModule:
        def getRawAxis(self, axis):
            return self.joy.getRawAxis(axis)
        
        def getRawButton(self, button):
            return self.joy.getRawButton(button)
        
        def getPOV(self):
            return self.joy.getPOV()
        
        def __init__(self, joy):
            self.joy = joy #down in my heart
        
    def _isPs4(self, joy):
        return joy.getAxisCount() == 6 and (joy.getRawAxis(3) < -0.1 or joy.getRawAxis(4) < -0.1)
    
    def _isPs3(self, joy):
        return False
    
    def _isLogitech(self, joy):
        return False
    
    def _isNormal(self, joy):
        return True

    def __init__(self, index):
        '''
        Constructor
        '''
        self.joy = index if type(index) is IntType else wpilib.Joystick(0)
        if self._isPs4(self.joy):
            self.module = self.WirelessPs4Module(self.joy)
        elif self._isPs3(self.joy):
            self.module = self.WirelessPs4Module(self.joy)
        else:
            self.module = self.NormalModule(self.joy)
            
    def getRawAxis(self, axis):
        return self.module.getRawAxis(axis)
    
    def getRawButton(self, button):
        return self.module.getRawButton(button)
    
    def getPOV(self):
        return self.module.getPOV()