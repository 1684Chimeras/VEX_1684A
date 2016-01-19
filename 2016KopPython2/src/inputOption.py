'''
Created on Jan 18, 2016

@author: Arhowk
'''

class InputOption(object):
    '''
    classdocs
    '''
    @staticmethod
    def button(joystick, button1):
        ret = InputOption(joystick)
        ret.useButton = True
        ret.button1 = button1
        ret.button2 = -1
        return ret
        
    
    @staticmethod
    def buttons(joystick, button1, button2):
        ret = InputOption(joystick)
        ret.useButton = True
        ret.button1 = button1
        ret.button2 = button2
        return ret
        
    @staticmethod
    def axis(joystick, axis):
        ret = InputOption(joystick)
        ret.useAxis = True
        ret.axis = axis
        return ret
    
    @staticmethod
    def triggers(joystick):
        ret = InputOption(joystick)
        ret.useTriggers = True 
        return ret
        
    @staticmethod
    def pov(joystick, deg1, deg2 = -2):
        ret = InputOption(joystick)
        ret.usePov = True 
        ret.deg1 = deg1
        ret.deg2 = deg2
        return ret

    def __value(self):
        if self.usePov:
            if self.joystick.getPOV() == self.deg1:
                return 1.0
            elif self.joystick.getPOV() == self.deg2:
                return -1.0
            else:
                return 0.0
        elif self.useAxis:
            return self.joystick.getRawAxis(self.axis)
        elif self.useButton:
            if self.button1 > 0 and self.joystick.getRawButton(self.button1):
                return 1.0
            elif self.button2 > 0 and self.joystick.getRawButton(self.button2):
                return -1.0
            else:
                return 0.0
        elif self.useTriggers:
            return self.joystick.getRawAxis(3) - self.joystick.getRawAxis(2)
        else:
            print("IDK WHAT HAPPENED LOL")
            return 0.0
    def toDouble(self): 
        return self.__value()
    
    def toBoolean(self):
        return False
    
    def __init__(self, joystick):
        '''
        Constructor
        '''
        self.joystick = joystick
        self.usePov = False
        self.useTriggers = False
        self.useAxis = False 
        self.useButton = False