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
#from wpilib.cameraserver import CameraServer

#robot experienc                                                                                                                                                                                                     e -8g crosing the 2012 bump

class MyRobot(wpilib.SampleRobot):
    
    class RobotMap:
        driveLeftA = 2
        driveLeftB = 3
        driveRightA = 0
        driveRightB = 1
        shooter = 4
        armLeft = 7
        armRight = 6
        
        pulley = 5
        tape = 0
        queue = 3
        innerIntake = 2
        outerIntake = 1
        
        armPot = 0
        rotateGyro = 1
        
        light_left = 0
        light_right = 1
        hasBallSwitch = 3
        hasBallSwitch2 = 1
    
    def robotInit(self):
        #Driver Camera
        #import wpilib.CameraServer
        #CameraServer.startAutomaticCapture(CameraServer.getInstance(), "cam0")
        
        
        '''Robot initialization function'''
        # object that handles basic drive operations
        #hello from github
        RobotMap = self.RobotMap
        wpilib.DriverStation.reportError("\nRobot Code Initialize", False)
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
        self.wasTelopRan = True
        self.shooterWasSet = False
        self.shooterSet = 0.0
      #  self.leftStick.setRumble(wpilib.Joystick.RumbleType.kLeftRumble_val, 0.8)
        self.auto_mode = 3
        self.auto_defense = 4
        self.auto_position = 3
        #self.dc = DashComm()
        wpilib.DriverStation.reportError("\nWaiting for auton selection...", False)
        #self.waitForAuton()
        
        
        #wpilib.Timer.delay(1000)
        
    def waitForAuton(self):
        buttonPressed = False
        update = False
        startClickedOnce = False
        selectClickedOnce = False
        
        j = oi.OI.joy0
        b = oi.OI
        
        defaultMode = 3
        defaultDefense = 4
        defaultPosition = 3
        
        mode = defaultMode
        defense = defaultDefense
        position = defaultPosition
        
        max_mode = 5
        max_defense = 8
        max_position = 5
        
        modes=["Do Nothing", "Cross and Score", "Cross", "Score", "Approach"]
        defenses = ["Shovel the Fries", "Drawbridge", "Guillotine", "Moat", "Sally Port", "Rough Terrain", "Bump", "Ramparts"]
        positions = ["Leftmost (low bar)", "Left", "Middle", "Right", "Rightmost"]
        
        wpilib.DriverStation.reportError("\n\n\n\n\nSelected Auton: " + modes[mode-1], False)
        wpilib.DriverStation.reportError("\nSelected Defense: " + defenses[defense-1], False)
        wpilib.DriverStation.reportError("\nSelected Position: " + positions[position-1], False)
        wpilib.DriverStation.reportError("\nUse A-B-X-Y-LB-RB to change these", False)
        wpilib.DriverStation.reportError("\nPress start twice to lock in & enable code", False)
        wpilib.DriverStation.reportError("\nPress select twice to use default code", False)
        
        locked = False
        print(not locked)
        print(not wpilib.DriverStation.getInstance().isEnabled())
        print(not self.isSimulation())
        print(not self.isOperatorControl())
        print(not self.isAutonomous())
        while(not locked and not wpilib.DriverStation.getInstance().isEnabled() and not self.isSimulation()): #todo- some FMS check
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
            if not locked:
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
                elif j.getRawButton(b.start) and False:
                    if not buttonPressed:
                        buttonPressed = True
                        if startClickedOnce:
                            #select auton
                            wpilib.DriverStation.reportError("\n\n\n\n\nSelected Auton: " + modes[mode-1], False)
                            wpilib.DriverStation.reportError("\nSelected Defense: " + defenses[defense-1], False)
                            wpilib.DriverStation.reportError("\nSelected Position: " + positions[position-1], False)
                            wpilib.DriverStation.reportError("\nSelection locked!", False)
                            self.auto_mode = mode
                            self.auto_defense = defense
                            self.auto_position = position
                            locked = True
                        else:
                            startClickedOnce = True
                            wpilib.DriverStation.reportError("\n\n\n\n\nSelected Auton: " + modes[mode-1], False)
                            wpilib.DriverStation.reportError("\nSelected Defense: " + defenses[defense-1], False)
                            wpilib.DriverStation.reportError("\nSelected Position: " + positions[position-1], False)
                            wpilib.DriverStation.reportError("\nAre you sure these are correct?", False)
                            wpilib.DriverStation.reportError("\nPress start again to confirm", False)
                    pass
                elif j.getRawButton(b.select):
                    if not buttonPressed:
                        buttonPressed = True
                        if selectClickedOnce:
                            #select auton
                            
                            mode = defaultMode
                            defense = defaultDefense
                            position = defaultPosition
                            wpilib.DriverStation.reportError("\n\n\n\n\nSelected Auton: " + modes[mode-1], False)
                            wpilib.DriverStation.reportError("\nSelected Defense: " + defenses[defense-1], False)
                            wpilib.DriverStation.reportError("\nSelected Position: " + positions[position-1], False)
                            wpilib.DriverStation.reportError("\nDefault auton loaded!", False)
                            self.auto_mode = mode
                            self.auto_defense = defense
                            self.auto_position = position
                            locked = True 
                        else:
                            selectClickedOnce = True
                            wpilib.DriverStation.reportError("\n\n\n\n\n\n\nAre you sure you want to load the default auton? " + modes[mode-1], False)
                            
                else:
                    buttonPressed = False
                    
                if update:
                    update = False
                    startClickedOnce = False
                    selectClickedOnce = False
                    wpilib.DriverStation.reportError("\n\n\n\n\nSelected Auton: " + modes[mode-1], False)
                    wpilib.DriverStation.reportError("\nSelected Defense: " + defenses[defense-1], False)
                    wpilib.DriverStation.reportError("\nSelected Position: " + positions[position-1], False)
                    wpilib.DriverStation.reportError("\nPress Start twice to confirm this selection", False)
                    wpilib.DriverStation.reportError("\n\nor press Select twice to input default auton", False)
                    
    def disabled(self):
        buttonPressed = False
        update = False
        startClickedOnce = False
        selectClickedOnce = False
        
        j = oi.OI.joy0
        b = oi.OI
        
        mode = self.auto_mode
        defense = self.auto_defense
        position = self.auto_position
        
        max_mode = 5
        max_defense = 8
        max_position = 5
        
        modes=["Do Nothing", "Cross and Score", "Cross", "Score", "Approach"]
        defenses = ["Shovel the Fries", "Drawbridge", "Guillotine", "Moat", "Sally Port", "Rough Terrain", "Bump", "Ramparts"]
        positions = ["Leftmost (low bar)", "Left", "Middle", "Right", "Rightmost"]
        
        defaultMode = 3
        defaultDefense = 4
        defaultPosition = 3
        locked = False
        self.wasRotatePID = False
        OI = oi.OI
        
        while self.isDisabled():
            
            oi.OI.refresh()
            self.camera.processImage()
        
           # if OI.rotate_pid.toBoolean() or OI.joy0.getRawButton(OI.y):
            #    wpilib.DriverStation.reportError("\nReset gyro offset {}".format(self.driveTrain.gyro.getAngle()), False)          
            #    if not self.wasRotatePID:
            #        self.wasRotatePID = True
            #        if OI.joy0.getRawButton(OI.y):
            #            self.driveTrain.pid_rotate(0)
            #        else:
            #            wpilib.DriverStation.reportError("\nRESET rotation offset {}".format(self.camera.getRotationOffset()), False)
            #            self.driveTrain.pid_rotate(self.camera.getRotationOffset())
             #   wpilib.DriverStation.reportError("\nReset rotation offset {}".format(self.camera.getRotationOffset()), False)    
                
            wpilib.SmartDashboard.putNumber("Potentiometer", self.flipper.getArmPosition())
            wpilib.SmartDashboard.putNumber("Potentiometer Raw", self.flipper.getPotValue())
            wpilib.SmartDashboard.putNumber("Gyro Reading", self.robotGyro.getAngle())
                                            
            wpilib.Timer.delay(0.005)
            
            if self.wasTelopRan and not locked:
            
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
                elif j.getRawButton(b.start) and False:
                    if not buttonPressed:
                        buttonPressed = True
                        if startClickedOnce:
                            #select auton
                            wpilib.DriverStation.reportError("\n\n\n\n\nSelected Auton: " + modes[mode-1], False)
                            wpilib.DriverStation.reportError("\nSelected Defense: " + defenses[defense-1], False)
                            wpilib.DriverStation.reportError("\nSelected Position: " + positions[position-1], False)
                            wpilib.DriverStation.reportError("\nSelection locked!", False)
                            self.auto_mode = mode
                            self.auto_defense = defense
                            self.auto_position = position
                            locked = True
                        else:
                            startClickedOnce = True
                            wpilib.DriverStation.reportError("\n\n\n\n\nSelected Auton: " + modes[mode-1], False)
                            wpilib.DriverStation.reportError("\nSelected Defense: " + defenses[defense-1], False)
                            wpilib.DriverStation.reportError("\nSelected Position: " + positions[position-1], False)
                            wpilib.DriverStation.reportError("\nAre you sure these are correct?", False)
                            wpilib.DriverStation.reportError("\nPress start again to confirm", False)
                    pass
                elif j.getRawButton(b.select):
                    if not buttonPressed:
                        buttonPressed = True
                        if selectClickedOnce:
                            #select auton
                            
                            mode = defaultMode
                            defense = defaultDefense
                            position = defaultPosition
                            wpilib.DriverStation.reportError("\n\n\n\n\nSelected Auton: " + modes[mode-1], False)
                            wpilib.DriverStation.reportError("\nSelected Defense: " + defenses[defense-1], False)
                            wpilib.DriverStation.reportError("\nSelected Position: " + positions[position-1], False)
                            wpilib.DriverStation.reportError("\nDefault auton loaded!", False)
                            self.auto_mode = mode
                            self.auto_defense = defense
                            self.auto_position = position
                            locked = True 
                        else:
                            selectClickedOnce = True
                            wpilib.DriverStation.reportError("\n\n\n\n\nAre you sure you want to load the default auton? " + modes[mode-1], False)
                            
                else:
                    buttonPressed = False
                    
                if update:
                    update = False
                    startClickedOnce = False
                    selectClickedOnce = False
                    self.auto_mode = mode
                    self.auto_defense = defense
                    self.auto_position = position
                    wpilib.DriverStation.reportError("\n\n\n\n\nSelected Auton: " + modes[mode-1], False)
                    wpilib.DriverStation.reportError("\nSelected Defense: " + defenses[defense-1], False)
                    wpilib.DriverStation.reportError("\nSelected Position: " + positions[position-1], False)
                    wpilib.DriverStation.reportError("\nPress Start twice to confirm this selection", False)
                    wpilib.DriverStation.reportError("\n\nor press Select twice to input default auton", False)
            #wpilib.DriverStation.reportError("peri",False)
            elif j.getRawButton(b.a) or j.getRawButton(b.b) or j.getRawButton(b.x) or j.getRawButton(b.y) or j.getRawButton(b.lb) or j.getRawButton(b.rb) or j.getRawButton(b.select) or j.getRawButton(b.start):
                if not buttonPressed:
                    buttonPressed = True
                    wpilib.DriverStation.reportError("\n\n\n\n\nSelected Auton: " + modes[mode-1], False)
                    wpilib.DriverStation.reportError("\nSelected Defense: " + defenses[defense-1], False)
                    wpilib.DriverStation.reportError("\nSelected Position: " + positions[position-1], False)
                    wpilib.DriverStation.reportError("\nSelections are locked", False) 
            else:
                buttonPressed = False
                
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
        #self.auto_manager.autonomousInit(self.auto_mode, self.auto_defense, self.auto_position)
        
        modes=["Do Nothing", "Cross and Score", "Cross", "Score", "Approach"]
        defenses = ["Shovel the Fries", "Drawbridge", "Guillotine", "Moat", "Sally Port", "Rough Terrain", "Bump", "Ramparts"]
        positions = ["Leftmost (low bar)", "Left", "Middle", "Right", "Rightmost"]
        
        wpilib.DriverStation.reportError("\n\n\n\n\nSelected Auton: " + modes[self.auto_mode-1], False)
        wpilib.DriverStation.reportError("\nSelected Defense: " + defenses[self.auto_defense-1], False)
        wpilib.DriverStation.reportError("\nSelected Position: " + positions[self.auto_position-1], False)
        self.auto_manager.autonomousInit(self.auto_mode, self.auto_defense, self.auto_position)
        print("Auto selections {} {} {}".format(self.auto_defense, self.auto_mode, self.auto_position))
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
        self.wasTelopRan = True
        
                            
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
                
            if OI.rotate_pid.toBoolean() or OI.joy0.getRawButton(OI.y):
                wpilib.DriverStation.reportError("\nReset gyro offset {}".format(self.driveTrain.gyro.getAngle()), False)          
                if not self.wasRotatePID:
                    self.wasRotatePID = True
                    if OI.joy0.getRawButton(OI.y):
                        self.driveTrain.pid_rotate(0)
                    else:
                        wpilib.DriverStation.reportError("\nRESET rotation offset {}".format(self.camera.getRotationOffset()), False)
                        self.driveTrain.pid_rotate(self.camera.getRotationOffset())
                wpilib.DriverStation.reportError("\nReset rotation offset {}".format(self.camera.getRotationOffset()), False)   
                self.driveTrain.pid_periodic(-OI.driver_move.toDouble())
            else:
                self.wasRotatePID = False
                self.driveTrain.arcadeDrive(self.deadband(-OI.driver_move.toDouble()) * driveFactor, self.deadband(-OI.driver_rotate.toDouble()) * driveFactor, squaredInputs = False)
            
            
            
            
            
            
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
                    self.flipper.pid_goto(126)
                    
                if OI.arm_pid_backward.toBoolean():
                    self.flipper.pid_goto(165)
                    
                if abs(OI.pulley.toDouble()) > 0.4:
                    self.flipper.pid_goto(205)
                    
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
