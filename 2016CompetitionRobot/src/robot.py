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
import time
from modules.queuee import Queue
from modules import driveTrain, intake, shooter, flipper, climber, camera
from wpilib.driverstation import DriverStation
from networktables import NetworkTable
from auton_manager import AutonManager

#robot experienc                                                                                                                                                                                                     e -8g crosing the 2012 bump

class MyRobot(wpilib.SampleRobot):
    
    class RobotMap:
        driveLeftA = 4
        driveLeftB = 5
        driveRightA = 6
        driveRightB = 7
        shooter = 3
        armLeft = 2
        armRight = 1
        
        pulley = 3
        tape = 8
        queue = 0
        innerIntake = 2
        outerIntake = 1
        
        armPot = 0
        rotateGyro = 1
    
    def robotInit(self):
        '''Robot initialization function'''
        # object that handles basic drive operations
        #hello from github
        RobotMap = self.RobotMap
        
        wpilib.DriverStation.reportError(oi.OI.newLine + "Robot Code Initialize", False)
     
        oi.OI.initialize()
        self.robotGyro = wpilib.AnalogGyro(RobotMap.rotateGyro)
        self.intake = intake.Intake(RobotMap.innerIntake,RobotMap.outerIntake)
        self.camera = camera.Camera()
        self.driveTrain = driveTrain.DriveTrain(RobotMap.driveLeftA,RobotMap.driveRightA,RobotMap.driveLeftB,RobotMap.driveRightB, self.robotGyro)
        self.queue = Queue(RobotMap.queue)
        self.flipper = flipper.Flipper(RobotMap.armLeft, RobotMap.armRight, RobotMap.armPot)
        self.climber = climber.Climber(RobotMap.pulley,RobotMap.tape)
        self.shooter = shooter.Shooter(self.camera,self.driveTrain, RobotMap.shooter)
     #   self.newEncoder = wpilib.SPI(1)
        self.robotAccel = wpilib.BuiltInAccelerometer()
        self.wasFlipperSet = False
        self.auto_manager = AutonManager(self.climber, self.driveTrain, self.flipper, self.intake, self.queue, self.shooter, self.camera)
        time.auton_start = 0
        
        self.mode = wpilib.SendableChooser()
        self.mode.addDefault("Do Nothing", 0)
        self.mode.addObject("Cross And Score", 1)
        self.mode.addObject("Cross", 2)
        self.mode.addObject("Score", 3)
        self.defense = wpilib.SendableChooser()
        self.defense.addDefault("Cheval de Frise", 0)
        self.defense.addObject("Drawbridge", 1)
        self.defense.addObject("Guillotine", 2)
        self.defense.addObject("Moat", 3)
        self.defense.addObject("Sally Port", 4)
        self.defense.addObject("Rough Terrain", 5)
        self.defense.addObject("Bump", 6)
        self.defense.addObject("Ramparts", 7)
        self.defensePosition = wpilib.SendableChooser()
        self.defensePosition.addDefault("Leftmost", 1)
        self.defensePosition.addObject("Left", 2)
        self.defensePosition.addObject("Middle", 3)
        self.defensePosition.addObject("Right", 4)
        self.defensePosition.addObject("Rightmost", 5)
        wpilib.SmartDashboard.putData("Mode", self.mode)
        wpilib.SmartDashboard.putData("Defense", self.defense)
        wpilib.SmartDashboard.putData("Defense Position", self.defensePosition)
        self.shooterWasSet = False
        self.shooterSet = 0.0
      #  self.leftStick.setRumble(wpilib.Joystick.RumbleType.kLeftRumble_val, 0.8)
      
    def disabled(self):
        while self.isDisabled():
            self.camera.processImage()
            oi.OI.refresh()
            wpilib.SmartDashboard.putNumber("Potentiometer", self.flipper.getArmPosition())
            wpilib.SmartDashboard.putNumber("Potentiometer Raw", self.flipper.getPotValue())
            wpilib.SmartDashboard.putNumber("Gyro Reading", self.robotGyro.getAngle())
                                            
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
        
    def autonomous(self):
        time.auton_start = time.time()
        self.auto_manager.autonomousInit(self.mode.getSelected(), self.defense.getSelected(), self.defensePosition.getSelected())
        while(self.isAutonomous() and self.isEnabled()):
            self.camera.processImage()
            self.auto_manager.autonomousPeriodic()
            wpilib.Timer.delay(0.005)
        
    def operatorControl(self):
        '''Runs the motors with tank steering'''
        OI = oi.OI
        #3 - left trigger
        #4 - right trigger
        self.shooterSet = 0.0
        self.shooterWasSet = False
        self.wasFlipperSet = True
        self.wasRotatePID = False
        while self.isOperatorControl() and self.isEnabled():
            wpilib.SmartDashboard.putNumber("Gyro Reading", self.robotGyro.getAngle())
            self.camera.processImage()
            #DRIVE TRAIN CODE
            driveFactor = 1
            
            if OI.drive_low.toBoolean():
                driveFactor = 0.7
                
            if OI.rotate_pid.toBoolean():
                if not self.wasRotatePID:
                    self.wasRotatePID = True
                    self.driveTrain.pid_rotate(self.camera.getRotationOffset())
                self.driveTrain.pid_periodic(-OI.driver_move.toDouble())
            else:
                self.wasRotatePID = False
                self.driveTrain.arcadeDrive(-OI.driver_move.toDouble() * driveFactor, -OI.driver_rotate.toDouble() * driveFactor)
            
            #FLIPPER
            #TODO - Re-insert PID to flipper
            if(abs(OI.flipper.toDouble()) > 0.25):
                self.flipper.set(OI.flipper.toDouble() * 0.5)
                self.wasFlipperSet = True
            else:
                if self.wasFlipperSet:
                    self.wasFlipperSet = False
                    self.flipper.pid_lock()
                
                if OI.arm_pid_off.toBoolean():
                    self.flipper.pid_goto(205)
                
                if OI.arm_pid_up.toBoolean():
                    self.flipper.pid_goto(90)
                    
                if OI.arm_pid_hover.toBoolean():
                    self.flipper.pid_goto(178)
                    
                if OI.arm_pid_diag.toBoolean():
                    self.flipper.pid_goto(135)
                    
                self.flipper.pid_goto()
                
            #END FLIPPER CODE
            
            #INTAKE
            if OI.outer_arm_only.toBoolean():
                self.intake.set(-OI.intake.toDouble(), -1)
            elif OI.queue.toDouble() != 0:
                self.intake.set(1,0)
            else:
                if OI.intake.toDouble() > 0.5:
                    self.intake.set(-0.5)
                elif OI.intake.toDouble() < -0.5:
                    self.intake.set(1)
                else:
                    self.intake.set(0)
                    
                #self.intake.set(-OI.intake.toDouble())
            if OI.queue.toDouble() == 0 and abs(OI.intake.toDouble()) > 0.5:
                self.queue.set(-1)
            else: #time to shot- 4sec
                self.queue.set(OI.queue.toDouble() * 0.4)  
                
            self.climber.setPulley(self.deadband(OI.pulley.toDouble()))
            self.climber.setTape(self.deadband(OI.tape.toDouble()))
            
            #SHOOTER
            #self.shooter.fullPowerToggle(OI.shooter_max_speed.toBoolean())
            self.shooter.changeOnToggle(OI.shooter.toDouble())
            #END SHOOTER
            
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
    
     #NetworkTable.setIPAddress("localhost")
     wpilib.run(MyRobot)
