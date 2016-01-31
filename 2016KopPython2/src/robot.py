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
from modules.queuee import Queue
from modules import driveTrain, intake, shooter, flipper, climber, camera
from wpilib.driverstation import DriverStation

#robot experienc                                                                                                                                                                                                     e -8g crosing the 2012 bump

class MyRobot(wpilib.SampleRobot):
    
    class RobotMap:
        driveLeftA = 1
        driveLeftB = 2
        driveRightA = 3
        driveRightB = 4
        shooter = 1
        armLeft = 7
        armRight = 8
        pulley = 10
        tape = 0
        queue = 9
        innerIntake = 6
        outerIntake = 5
        
        armPot = 3
    
    def robotInit(self):
        '''Robot initialization function'''
        print("Initialization Started")
        # object that handles basic drive operations
        #hello from github
        RobotMap = self.RobotMap
        
        wpilib.DriverStation.reportError(oi.OI.newLine + "Robot Code Initialize", False)
     
        self.intake = intake.Intake(RobotMap.innerIntake,RobotMap.outerIntake)
        self.shooter = shooter.Shooter(RobotMap.shooter)
        self.driveTrain = driveTrain.DriveTrain(RobotMap.driveLeftA,RobotMap.driveRightA,RobotMap.driveLeftB,RobotMap.driveRightB)
        self.queue = Queue(RobotMap.queue)
        self.flipper = flipper.Flipper(RobotMap.armLeft, RobotMap.armRight, RobotMap.armPot)
        self.climber = climber.Climber(RobotMap.pulley,RobotMap.tape)
        self.camera = camera.Camera()
        self.robotAccel = wpilib.BuiltInAccelerometer()
        
        
        self.shooterWasSet = False
        self.shooterSet = 0.0
      #  self.leftStick.setRumble(wpilib.Joystick.RumbleType.kLeftRumble_val, 0.8)
        oi.OI.initialize()
        print("Initialization Successfulrc")
    def disabled(self):
        while self.isDisabled():
            
            oi.OI.refresh()
            
            wpilib.SmartDashboard.putNumber("Potentiometer", self.flipper.getArmPosition())
            wpilib.SmartDashboard.putNumber("Potentiometer Raw", self.flipper.getPotValue())
                                            
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
 
            driveFactor = 1
            
            if OI.drive_low.toBoolean():
                driveFactor = 0.7
                
            self.driveTrain.arcadeDrive(-OI.driver_move.toDouble() * driveFactor, -OI.driver_rotate.toDouble() * driveFactor)
            if(abs(OI.flipper.toDouble()) > 0.25):
                self.flipper.set(OI.flipper.toDouble() * 0.4)
            else:
                self.flipper.pid_stay()
            self.intake.set(-OI.intake.toDouble())
            if OI.queue.toDouble() == 0 and OI.intake.toDouble() != 0:
                self.queue.set(-0.5)
            else: #time to shot- 4sec
                self.queue.set(OI.queue.toDouble() * 0.4)  
                
            self.climber.setPulley(self.deadband(OI.pulley.toDouble()))
            self.climber.setTape(self.deadband(OI.tape.toDouble()))
            self.shooter.changeOnToggle(OI.shooter.toDouble())
            
            
            '''
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
            '''
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
