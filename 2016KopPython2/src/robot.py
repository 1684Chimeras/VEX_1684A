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
import oi
import modules.driveTrain
from modules import driveTrain, intake, queue, shooter, flipper, climber
from wpilib.driverstation import DriverStation

#robot experience -8g crosing the 2012 bump

class MyRobot(wpilib.SampleRobot):
    
    def robotInit(self):
        '''Robot initialization function'''
        print("Initialization Started")
        # object that handles basic drive operations
        #hello from github
        wpilib.DriverStation.reportError(oi.OI.newLine + "Robot Code Initialize", False)
     
        self.intake = intake.Intake(3)
        self.shooter = shooter.Shooter(1)
        self.driveTrain = driveTrain.DriveTrain(0,1)
        self.queue = queue.Queue(5)
        self.flipper = flipper.Flipper(4)
        self.climber = climber.Climber(6)
        self.robotAccel = wpilib.BuiltInAccelerometer()
        self.climberRuler = wpilib.VictorSP(8)
        
        self.shooterWasSet = False
        self.shooterSet = 0.0
        # joysticks 1 & 2 on the driver station
        self.leftStick = wpilib.Joystick(0)
        self.rightStick = wpilib.Joystick(1)
      #  self.leftStick.setRumble(wpilib.Joystick.RumbleType.kLeftRumble_val, 0.8)
        oi.OI.initialize()
        print("Initialization Successfulrc")
    def disabled(self):
        while self.isDisabled():
            
            oi.OI.refresh()
            
            wpilib.Timer.delay(0.005)
        
    def generate(self, stick, a, b=-1):
        if(b == -1):
            return 1.0 if stick.getRawButton(a) else 0
        else:
            return 1.0 if stick.getRawButton(a) else (-1.0 if self.leftStick.getRawButton(b) else 0.0)
    
    def deadband(self, val):
        if val < 0.1 and val > -0.1:
            return 0
        elif val > 0.1:
            return (val - 0.1) / 0.9
        else:
            return (val + 0.1) / 0.9
        
    def operatorControl(self):
        '''Runs the motors with tank steering'''
        OI = oi.OI
        #3 - left trigger
        #4 - right trigger
        self.shooterSet = 0.0
        self.shooterWasSet = False
        while self.isOperatorControl() and self.isEnabled():
#             
                
            self.driveTrain.arcadeDrive(OI.driver_move.toDouble(), -OI.driver_rotate.toDouble())
            self.flipper.set(OI.flipper.toDouble())
            self.intake.set(-OI.intake.toDouble() * 0.4)
            if OI.queue.toDouble() == 0 and OI.intake.toDouble() != 0:
                self.queue.set(-0.7)
            else:
                self.queue.set(OI.queue.toDouble())  
            self.climber.set(self.deadband(OI.pulley.toDouble()))
            self.climberRuler.set(self.deadband(OI.tape.toDouble()))
              
            shooterSet = OI.shooter.toDouble()
            print(shooterSet)
            if(shooterSet != 0.0 and not self.shooterWasSet):
                if(self.shooterSet == 0.0):
                    self.shooterSet = shooterSet
                else:
                    self.shooterSet = 0.0
                     
                self.shooterWasSet = True
            elif(shooterSet == 0.0 and self.shooterWasSet):
                self.shooterWasSet = False
                     
            self.shooter.set(-self.shooterSet * 7.6)           
#old stuff
#             wpilib.SmartDashboard.putNumber("z-accel", self.robotAccel.getZ())
#             self.driveTrain.arcadeDrive(self.leftStick.getRawAxis(5), -self.leftStick.getRawAxis(0))
#             
#             flipperSet = (self.leftStick.getRawAxis(3)  -self.leftStick.getRawAxis(2)) / -1.2
#             self.flipper.set(flipperSet)
#             
#             intakeSet = self.generate(self.leftStick, 2,3)
#             self.intake.set(-intakeSet * 0.6)
#         
#             queueSet = self.generate(self.leftStick, 1,4)
#             
#             if(intakeSet > 0.1 and queueSet == 0.0):
#                 queueSet = 0.25
#                 
#             self.queue.set(-queueSet)
#             
#             climberRulerSet = 1.0 if self.leftStick.getPOV() == 0 else (-0.6 if self.leftStick.getPOV() == 180 else 0.0)
#             self.climberRuler.set(-climberRulerSet)
#             print("Climber Ruer set ")
#             
#             climberWinchSet = 1.0 if self.leftStick.getPOV() == 90 else (-1.0 if self.leftStick.getPOV() == 270 else 0.0)
#             self.climber.set(climberWinchSet)
#             
#             shooterSet = self.generate(self.rightStick, 6,5)
#             
#             if(shooterSet != 0.0 and not self.shooterWasSet):
#                 if(self.shooterSet == 0.0):
#                     self.shooterSet = shooterSet
#                 else:
#                     self.shooterSet = 0.0
#                     
#                 self.shooterWasSet = True
#             elif(shooterSet == 0.0 and self.shooterWasSet):
#                 self.shooterWasSet = False
#                     
#             self.shooter.set(-self.shooterSet * 7.6)
            
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
