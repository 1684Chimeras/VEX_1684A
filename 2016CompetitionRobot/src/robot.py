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
from dashcomm import DashComm

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
        
        light_left = 6
        light_right = 7
        hasBallSwitch = 3
        hasBallSwitch2 = 1
    
    def robotInit(self):
        '''Robot initialization function'''
        # object that handles basic drive operations
        #hello from github
        RobotMap = self.RobotMap
        print("Robot Code Initialize")
        #DashComm.print("Robot Code Initialize")
        set = time.time()
        import networktables
        networktables.NetworkTable.getTable("/GRIP/")
        DashComm.print(time.time() - set)
        oi.OI.initialize()
        self.blueLight = wpilib.Solenoid(RobotMap.light_left)
        self.blueLightB = wpilib.Solenoid(RobotMap.light_right)
        self.hasBallSwitch = wpilib.AnalogInput(RobotMap.hasBallSwitch)
        self.hasBallSwitch2 = wpilib.DigitalInput(RobotMap.hasBallSwitch2)
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
        self.lastPulleyTime = 0
        self.pulleyState = False
        self.auto_manager = AutonManager(self.climber, self.driveTrain, self.flipper, self.intake, self.queue, self.shooter, self.camera)
        time.auton_start = 0
        
        self.mode = wpilib.SendableChooser()
        self.mode.addObject("Not Selected", 0)
        self.mode.addObject("Do Nothing", 1)
        self.mode.addObject("Cross And Score", 2)
        self.mode.addDefault("Cross", 3)
        self.mode.addObject("Score", 4)
        self.mode.addObject("Approach", 5)
        self.defense = wpilib.SendableChooser()
        self.defense.addObject("Not Selected", 0)
        self.defense.addObject("Cheval de Frise", 1)
        self.defense.addObject("Drawbridge", 2)
        self.defense.addObject("Guillotine", 3)
        self.defense.addObject("Moat", 4)
        self.defense.addObject("Sally Port", 5)
        self.defense.addObject("Rough Terrain", 6)
        self.defense.addObject("Bump", 7)
        self.defense.addDefault("Ramparts", 8)
        self.defensePosition = wpilib.SendableChooser()
        self.defensePosition.addObject("Not Selected", 0)
        self.defensePosition.addObject("Leftmost", 1)
        self.defensePosition.addObject("Left", 2)
        self.defensePosition.addDefault("Middle", 3)
        self.defensePosition.addObject("Right", 4)
        self.defensePosition.addObject("Rightmost", 5)
        wpilib.SmartDashboard.putData("Mode", self.mode)
        wpilib.SmartDashboard.putData("Defense", self.defense)
        wpilib.SmartDashboard.putData("Defense Position", self.defensePosition)
        self.shooterWasSet = False
        self.shooterSet = 0.0
      #  self.leftStick.setRumble(wpilib.Joystick.RumbleType.kLeftRumble_val, 0.8)
      
        #self.dc = DashComm()
        DashComm.print("Begin Delay")
        #wpilib.Timer.delay(1000)
        
    def disabled(self):
        buttonPressed = False
        update = False
        startClickedOnce = False
        selectClickedOnce = False
        
        j = oi.OI.joy0
        b = oi.OI
        
        mode = 1
        defense = 1
        position = 1
        
        max_mode = 5
        max_defense = 8
        max_position = 5
        
        modes=["Do Nothing", "Cross and Score", "Cross", "Score", "Approach"]
        defenses = []
        positions = []
        
        while self.isDisabled():
            self.camera.processImage()
            oi.OI.refresh()
            wpilib.SmartDashboard.putNumber("Potentiometer", self.flipper.getArmPosition())
            wpilib.SmartDashboard.putNumber("Potentiometer Raw", self.flipper.getPotValue())
            wpilib.SmartDashboard.putNumber("Gyro Reading", self.robotGyro.getAngle())
                                            
            wpilib.Timer.delay(0.005)
            
            #A - Mode Down
            #Y - Mode Up
            #B - Defense Up
            #X - Defense Down
            #RB - Position Up
            #LB - Position Down
            #Start (2x) - Confirm Selection
            #Select (2x) - Default Auton
            
            if j.getRawButton(b.a):
                if not buttonPressed:
                    buttonPressed = True
                    update = True
                    mode = mode - 1
                    if mode < 1:
                        mode = max_mode
            elif j.getRawButton(b.y):
                if not buttonPressed:
                    buttonPressed = True
                    update = True
                    mode = mode + 1
                    if mode > max_mode:
                        mode = 1
            elif j.getRawButton(b.x):
                if not buttonPressed:
                    buttonPressed = True
                    update = True
                    defense = defense - 1
                    if defense < 1:
                        defense = max_defense
            elif j.getRawButton(b.b):
                if not buttonPressed:
                    buttonPressed = True
                    update = True
                    defense = defense + 1
                    if defense > max_defense:
                        defense = 1
            elif j.getRawButton(b.lb):
                if not buttonPressed:
                    buttonPressed = True
                    update = True
                    position = position - 1
                    if position < 1:
                        position = max_position
            elif j.getRawButton(b.rb):
                if not buttonPressed:
                    buttonPressed = True
                    update = True
                    position = position + 1
                    if position > max_position:
                        position = 1
            elif j.getRawButton(b.start):
                pass
            elif j.getRawButton(b.select):
                pass
            else:
                buttonPressed = False
                
            if update:
                update = False
                startClickedOnce = False
                selectClickedOnce = False
                wpilib.DriverStation.reportError("\n\n\nSelected Auton: " + modes[mode-1], False)
                wpilib.DriverStation.reportError("\nSelected Defense: " + defenses[defense-1], False)
                wpilib.DriverStation.reportError("\nSelected Position: " + positions[position-1], False)
                wpilib.DriverStation.reportError("\nPress Start twice to confirm this selection", False)
                wpilib.DriverStation.reportError("\n\nor press Select twice to input default auton", False)
        
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
        #if not self.dc.validData():
        #    print("DashComm Not Valid Data")
            self.auto_manager.autonomousInit(self.mode.getSelected(), self.defense.getSelected(), self.defensePosition.getSelected())
        #else:
        #    print("DashComm Valid")
        #    self.auto_manager.autonomousInit(self.dc.getMode(), self.dc.getDefense(), self.dc.getPosition())
        self.intake.set(0)
        self.shooter.set(0)
        self.queue.set(0)
        self.driveTrain.arcadeDrive(0,0)
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
        self.hasSeizure = False
        
        armGoOut = False
        armPidOn = False
        armTime = 0
        armTimeout = 2
        #arm
        
        hadBall = False
        hadBallTime = 0
        while self.isOperatorControl() and self.isEnabled():
            start = time.time()
            if(self.hasBallSwitch.getVoltage() < 0.2 or not self.hasBallSwitch2.get()):
                if not hadBall:
                    hadBall = True
                    hadBallTime = time.time()
                self.blueLight.set(True)
                self.blueLightB.set(True)
            elif abs(OI.pulley.toDouble()) > 0.15:
                hadBall = False
                self.hasSeizure = True
                if time.time() - self.lastPulleyTime > 1.0/6.0:
                    self.pulleyState = not self.pulleyState
                    self.blueLight.set(self.pulleyState)
                    self.blueLightB.set(not self.pulleyState)
                    self.lastPulleyTime = time.time()
            elif abs(OI.tape.toDouble()) > 0.15:
                hadBall = False
                if time.time() - self.lastPulleyTime > 1.0/3.0:
                    self.pulleyState = not self.pulleyState
                    self.blueLight.set(self.pulleyState)
                    self.blueLightB.set(self.pulleyState)
                    self.lastPulleyTime = time.time()
            else:
                hadBall = False
                if self.hasSeizure:
                    self.auto_manager.lightRoutine(self.blueLight, self.blueLightB)
                else:
                    self.blueLight.set(False)
                    self.blueLightB.set(False)
                    
            if hadBall and hadBallTime + 1 > time.time():
                oi.OI.ballVibrating = True
                oi.OI.driverVibrate(0.7, -0.7)
            elif oi.OI.ballVibrating:
                oi.OI.ballVibrating = False
                oi.OI.driverVibrate(0,0)
                
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
                self.flipper.driver_control(OI.flipper.toDouble() * 0.8)
                self.wasFlipperSet = True
            else:
                if self.wasFlipperSet:
                    self.wasFlipperSet = False
                    self.flipper.pid_lock()
                
                if OI.arm_pid_off.toBoolean():
                    self.flipper.pid_goto(205)
                
                if OI.arm_pid_up.toBoolean():
                    self.flipper.pid_goto(90)
                    
                if OI.arm_pid_slam.toBoolean():
                    self.flipper.pid_goto(82)
                    
                if OI.arm_pid_hover.toBoolean():
                    self.flipper.pid_goto(173)
                    
                if OI.arm_pid_diag.toBoolean():
                    self.flipper.pid_goto(127)
                    
                if OI.arm_pid_backward.toBoolean():
                    self.flipper.pid_goto(165)
                self.flipper.pid_goto()
                
            #END FLIPPER CODE
            
            #INTAKE
            if OI.outer_arm_only.toBoolean():
                self.intake.set(OI.intake.toDouble(), 1)
            elif OI.joy0.getPOV() == OI.north:
                self.intake.set(-0.75,0)
            elif OI.joy0.getPOV() == OI.east:
                self.intake.set(-1,0)
            elif OI.joy0.getPOV() == OI.west:
                self.intake.set(-0.25,0)
            elif OI.queue.toDouble() != 0:
                self.intake.set(-1,0)
            else:
                if OI.intake.toDouble() > 0.5:
                    self.intake.set(-1)
                elif OI.intake.toDouble() < -0.5:
                    self.intake.set(1)
                else:
                    self.intake.set(0)
                    
                #self.intake.set(-OI.intake.toDouble())
            if OI.queue.toDouble() == 0 and abs(OI.intake.toDouble()) > 0.5:
                self.queue.set(-1)
            else: #time to shot- 4sec
                self.queue.set(OI.queue.toDouble() * 0.4)  
            
            if OI.tape.toDouble() > 0.5:
                if not armPidOn or (armPidOn and not armGoOut):
                    armGoOut = True
                    armPidOn = True
                    armTime = time.time()
            elif OI.tape.toDouble() < -0.5:
                if not armPidOn or (armPidOn and armGoOut):
                    armGoOut = False
                    armPidOn = True
                    armTime = time.time()
                    
            if armPidOn:
                if time.time() - armTimeout > armTime:
                    armPidOn = False
                else:
                    if armGoOut:
                        self.climber.setTape(1)
                    else:
                        self.climber.setTape(-1)
            else:
                self.climber.setTape(0)
            self.climber.setPulley(self.deadband(OI.pulley.toDouble()))
            #self.climber.setTape(self.deadband(OI.tape.toDouble()))
            
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
            
            if time.time() - start > 0.005:
                wpilib.Timer.delay(0.001)
            else:
                wpilib.Timer.delay(0.005 - (time.time() - start)) # wait for a motor update time
            
if __name__ == '__main__':
     
      #NetworkTable.setIPAddress("localhost")
     wpilib.run(MyRobot)
