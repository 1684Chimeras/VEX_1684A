#!/usr/bin/env python3
'''
    This is a demo program showing the use of the RobotDrive class,
    specifically it contains the code necessary to operate a robot with
    tank drive.
    
    WARNING: While it may look like a good choice to use for your code if
    you're inexperienced, don't. Unless you know what you are doing, complex
    code will be much more difficult under this system. Use IterativeRobot
    or Command-Based instead if you're new.
'''

import wpilib

class MyRobot(wpilib.SampleRobot):
    
    def robotInit(self):
        '''Robot initialization function'''
        print("Initialization Started")
        # object that handles basic drive operations
        self.myRobot = wpilib.RobotDrive(1,0)
        self.myRobot.setExpiration(0.651)
        self.intake = wpilib.VictorSP(2)
        self.tower = wpilib.VictorSP(3)
        self.tower_right = wpilib.VictorSP(4)
        self.idk_what_this_is = wpilib.VictorSP(5)
        self.talon = wpilib.CANTalon(1)
        self.talon.changeControlMode(wpilib.CANTalon.ControlMode.PercentVbus)
        
        # joysticks 1 & 2 on the driver station
        self.leftStick = wpilib.Joystick(0)
        self.rightStick = wpilib.Joystick(1)
        
        print("Initialization Successful")
        
    def operatorControl(self):
        '''Runs the motors with tank steering'''
        
        self.myRobot.setSafetyEnabled(True)
        #3 - left trigger
        #4 - right trigger
        while self.isOperatorControl() and self.isEnabled():
            self.myRobot.arcadeDrive(self.leftStick.getRawAxis(5), -self.leftStick.getRawAxis(0), True)
            towerSet = (self.leftStick.getRawAxis(3)  -self.leftStick.getRawAxis(2)) / -1.2
            
            self.tower_right.set(towerSet)
            
            flipperSet = 1.0 if self.leftStick.getRawButton(2) else (-1.0 if self.leftStick.getRawButton(3) else 0.0)
            self.tower.set(-flipperSet)
            print(flipperSet)
            
            idkSet = 1.0 if self.leftStick.getRawButton(1) else (-1.0 if self.leftStick.getRawButton(4) else 0.0)
            self.idk_what_this_is.set(-idkSet)
            
            shooterSet = 1.0 if self.leftStick.getRawButton(6) else (-1.0 if self.leftStick.getRawButton(5) else  0.0)
        
            self.talon.set(-shooterSet)
            wpilib.Timer.delay(0.005) # wait for a motor update time
            
if __name__ == '__main__':
     wpilib.run(MyRobot)
