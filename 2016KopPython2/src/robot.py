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

from modules import driveTrain, intake, queue, shooter, flipper



class MyRobot(wpilib.SampleRobot):
    
    def robotInit(self):
        '''Robot initialization function'''
        print("Initialization Started")
        # object that handles basic drive operations
        #hello from github
        
        self.intake = intake.Intake(3)
        self.shooter = shooter.Shooter(1)
        self.driveTrain = driveTrain.DriveTrain(1,0)
        self.queue = queue.Queue(5)
        self.flipper = flipper.Flipper(4)
        
        self.shooterWasSet = False
        
        # joysticks 1 & 2 on the driver station
        self.leftStick = wpilib.Joystick(0)
        self.rightStick = wpilib.Joystick(1)
        
        print("Initialization Successful")
        
    def generate(self, a, b=-1):
        if(b == -1):
            return 1.0 if self.leftStick.getRawButton(a) else 0
        else:
            return 1.0 if self.leftStick.getRawButton(a) else (-1.0 if self.leftStick.getRawButton(b) else 0.0)
    
    def operatorControl(self):
        '''Runs the motors with tank steering'''
        
        self.myRobot.setSafetyEnabled(True)
        #3 - left trigger
        #4 - right trigger
        while self.isOperatorControl() and self.isEnabled():
            
            self.driveTrain.arcadeDrive(self.leftStick.getRawAxis(5), -self.leftStick.getRawAxis(0))
            
            flipperSet = (self.leftStick.getRawAxis(3)  -self.leftStick.getRawAxis(2)) / -1.2
            self.flipper.set(flipperSet)
            
            intakeSet = self.generate(2,3)
            self.tower.set(-intakeSet)
            
            queueSet = self.generate(1,4)
            self.queue.set(-queueSet)
            
            shooterSet = self.generate(6,5)
            
            if(shooterSet != 0.0 and not self.shooterWasSet):
                if(self.shooterSet == 0.0):
                    self.shooterSet = shooterSet
                else:
                    self.shooterSet = 0.0
                    
                self.shooterWasSet = True
            elif(shooterSet == 0.0 and self.shooterWasSet):
                self.shooterWasSet = False
                    
            self.shooter.set(-self.shooterSet)
            
#
#             intakeSet = 1.0 if self.leftStick.getRawButton(2) else (-1.0 if self.leftStick.getRawButton(3) else 0.0)
#             self.tower.set(-intakeSet)
#             
#             queue = 1.0 if self.leftStick.getRawButton(1) else (-1.0 if self.leftStick.getRawButton(4) else 0.0)
#             self.queue.set(-queue)
#             
#             shooterSet = 1.0 if self.leftStick.getRawButton(6) else (-1.0 if self.leftStick.getRawButton(5) else  0.0)
#             self.shooter.set(-shooterSet)
            
            
            wpilib.Timer.delay(0.005) # wait for a motor update time
            
if __name__ == '__main__':
     wpilib.run(MyRobot)
