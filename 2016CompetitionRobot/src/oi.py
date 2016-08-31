'''
Created on Jan 18, 2016

@author: Arhowk
'''
import wpilib
import input_option
from input_option import InputOption

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
    
    newLine = "                                                                                                                                                                                                                                                                                "
    
    @staticmethod
    def initializeXboxDoubleController():
        driver = OI.joy0
        operator = OI.joy1
        #tableEx = [["squaredInputs","1"], ["scalar","2"]]
        
        OI.intake = InputOption.triggers(driver)
        #OI.intake = InputOption.buttons(driver, OI.b, OI.x)
        OI.queue = InputOption.buttons(driver, OI.lb, OI.a)
        OI.shooter = InputOption.button(driver, OI.rb)
        OI.shooter_max_speed = InputOption.button(driver, OI.start)
        OI.rotate_pid = InputOption.button(driver, OI.b)
        OI.outer_arm_only = InputOption.button(driver, OI.x)
        
        OI.drive_low = InputOption.button(driver, OI.select)
        OI.driver_move = InputOption.axis(driver, OI.ly)
        OI.driver_rotate = InputOption.axis(driver, OI.rx)
        
        
        OI.pulley = InputOption.axis(operator, OI.ly)
        OI.tape = InputOption.axis(operator, OI.ry)
        OI.flipper = InputOption.triggers(operator)
        
        OI.arm_pid_off = InputOption.button(operator, OI.a)
        OI.arm_pid_up = InputOption.button(operator, OI.y)
        OI.arm_pid_hover = InputOption.button(operator, OI.b)
        OI.arm_pid_diag =InputOption.button(operator, OI.x)
        OI.arm_pid_slam =InputOption.pov(operator, OI.east)
        OI.arm_pid_backward =InputOption.pov(operator, OI.west)
        
        OI.arm_pid_down_toggle = InputOption.nothing()
        OI.arm_pid_climb_toggle = InputOption.nothing()
        
    
    @staticmethod
    def initializeXboxSingleController():
        driver = OI.joy0
        #tableEx = [["squaredInputs","1"], ["scalar","2"]]
        
        OI.intake = InputOption.triggers(driver)
        #OI.intake = InputOption.buttons(driver, OI.b, OI.x)
        OI.queue = InputOption.buttons(driver, OI.lb, OI.a)
        OI.shooter = InputOption.button(driver, OI.rb)
        OI.shooter_max_speed = InputOption.button(driver, OI.start)
        OI.rotate_pid = InputOption.button(driver, OI.b)
        OI.outer_arm_only = InputOption.button(driver, OI.x)
        
        OI.drive_low = InputOption.button(driver, OI.select)
        OI.driver_move = InputOption.axis(driver, OI.ly)
        OI.driver_rotate = InputOption.axis(driver, OI.rx)
        
        
        OI.pulley = InputOption.nothing()
        OI.tape = InputOption.nothing()
        OI.flipper = InputOption.nothing()
        
        OI.arm_pid_off = InputOption.pov(driver, OI.south)
        OI.arm_pid_up = InputOption.pov(driver, OI.north)
        OI.arm_pid_hover = InputOption.nothing()
        OI.arm_pid_diag =InputOption.pov(driver, OI.east)
        OI.arm_pid_slam =InputOption.nothing()
        OI.arm_pid_backward =InputOption.nothing()
        
        OI.arm_pid_down_toggle = InputOption.nothing()
        OI.arm_pid_climb_toggle = InputOption.nothing()
    
    @staticmethod
    def isDemoMode():
        return True
    
    @staticmethod
    def driverVibrate(left,right):
        OI.joy0.setRumble(OI.joy0.RumbleType.kLeftRumble_val, left)
        OI.joy0.setRumble(OI.joy0.RumbleType.kRightRumble_val, right)
    
    @staticmethod
    def initialize():
        OI.joy0 = wpilib.Joystick(0)
        OI.joy1 = wpilib.Joystick(1)
        OI.joy2 = wpilib.Joystick(2)
        OI.joy3 = wpilib.Joystick(3)
        OI.ballVibrating = False
        OI.mode = -1
        OI.refresh()
        
    @staticmethod
    def refresh():
        if OI.joy1.getAxisCount() < 3:
            if OI.mode != 1:
                wpilib.DriverStation.reportError("                                                                                                                                                                                            Single Controller Mode\r\n\r\n", False)
                OI.initializeXboxSingleController()
                OI.mode = 1
        else:
            if OI.mode != 2:
                wpilib.DriverStation.reportError("\r\n\r\n                                                                                                                                                                                                                Double Controller Mode\r\n\r\n", False)
                OI.initializeXboxDoubleController()
                OI.mode = 2
        