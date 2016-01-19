'''
Created on Jan 18, 2016

@author: Arhowk
'''
import wpilib
import inputOption
from inputOption import InputOption

class OI(object):
    '''
    classdocs
    '''
    a = 1
    b = 2
    x = 3
    y = 4
    lb = 5
    rb = 6
    select = 7
    start = 8
    lc = 9
    rc = 10
    
    lx = 0
    ly = 1
    lt = 2
    rt = 3
    rx = 4
    ry = 5
    
    north = 0
    east = 90
    south = 180
    west = 270
    
    @staticmethod
    def initializeXboxSingleController():
        OI.joystick = wpilib.Joystick(0)
        joystick = OI.joystick
        #tableEx = [["squaredInputs","1"], ["scalar","2"]]
        
        OI.intake = InputOption.buttons(joystick, OI.b, OI.x)
        OI.queue = InputOption.buttons(joystick, OI.y, OI.a)
        OI.shooter = InputOption.button(joystick, OI.rb)
        OI.pulley = InputOption.pov(joystick, OI.north, OI.south)
        OI.tape = InputOption.pov(joystick, OI.east, OI.west)
        
        OI.driver_move = InputOption.axis(joystick, OI.ry)
        OI.driver_rotate = InputOption.axis(joystick, OI.lx)
    
    @staticmethod
    def initialize():
        OI.initializeXboxSingleController()