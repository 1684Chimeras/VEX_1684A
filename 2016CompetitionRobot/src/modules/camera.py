'''
Created on Jan 23, 2016

@author: Arhowk
'''

import wpilib
import subprocess
import _thread
from dashcomm import DashComm
from networktables import NetworkTable
from networktables import NumberArray

class Camera(object):
    '''
    classdocs
    '''
    
    h_min =0
    h_max = 0
    
    s_min = 0
    s_max = 0
    
    v_min = 0
    v_max = 0
    
    kernel_size = 3
    erode_iterations = 1
    dilate_iterations = 1
    
    #150/full power- center
    
    
    camera_width = 240
    camera_height = 320
    center_x = 122
    center_y = 150
    angle_of_camera = 67
    degrees_per_x_error = -angle_of_camera / camera_width
    time_per_y_error = 1
    
    def _getArray(self, key):
        beta = NumberArray()
        self.table.retrieveValue(key, beta)
        return beta

    def processImage(self):
        #print("PROCESS IMAGE")
        #print("What idiot just called the camera.processImage function?")
        #if True:
         #   return
        self.rotateError = -5000
        self.gripWorking = False
        try:
            beta = self._getArray("area")
            x = self._getArray("centerX")
            y = self._getArray("centerY") 
            self.largestArea = 0
            self.largestIndex = -1
            for index in range(len(beta)):
                if beta[index] > self.largestArea:
                    self.largestIndex = index
                    self.largestArea = beta[index]
            if self.largestIndex != -1:
                self.gripWorking = True
                wpilib.SmartDashboard.putNumber("Largest Area", beta[self.largestIndex])
                wpilib.SmartDashboard.putNumber("Largest x", x[self.largestIndex])
                wpilib.SmartDashboard.putNumber("Largest y", y[self.largestIndex])
                wpilib.SmartDashboard.putNumber("X Error", self.center_x - x[self.largestIndex])
                wpilib.SmartDashboard.putNumber("Rotate Error", self.degrees_per_x_error * (self.center_x - x[self.largestIndex]))
                wpilib.SmartDashboard.putNumber("Y Error", self.center_y - y[self.largestIndex])
                
                self.rotateError = self.degrees_per_x_error * (self.center_x - x[self.largestIndex])
                self.y = y[self.largestIndex]
        except KeyError:
            pass
        except IndexError:
            pass
        
        if self.rotateError == -500:
            self.gripWorking = False
        else:
            self.gripWorking = True 
    
    def isGripWorking(self):
        return self.gripWorking
    
    def getPixelXOffset(self):
        
        return
    
    def getY(self):
        return self.y / self.camera_height
    
    def getIntakeOffset(self):
        pass
    
    def getRotationOffset(self):
        return self.rotateError
    
    def getZOffset(self):
        return 0.0
    
    def startProcess(self, literally, nothing):
        import cv2
        import numpy as np
        import urllib.request
        
        while 1:
            try:
                DashComm.print("Starting Process")
                self.rotateError = -5000
                stream = urllib.request.urlopen('http://10.16.84.11/mjpg/video.mjpg')
                #
                #self.dataValid = False
                #video_capture = cv2.VideoCapture(0)
                #print("Capture Done")
                #videoStreamAddress = "http://10.16.84.130/mjpg/video.mjpg";
                
                #if video_capture.open(videoStreamAddress):
                   # print("Capture Success")
                if True:
                    feedBytes = bytes()
                    self.cvWorking = False
                    while 1:
                        frame = ''
                        i = 1
                        DashComm.print("Grab File")
                        while i < 100000:
                            i = i + 1
                            feedBytes = feedBytes + stream.read(1024)
                            a = feedBytes.find(b'\xff\xd8')
                            b = feedBytes.find(b'\xff\xd9')
                            if a != -1 and b != -1:
                                DashComm.print("GOOD : Icount {} {} {}".format(i,a,b))
                                #DashComm.print(feedBytes)
                                jpg = feedBytes[a:b+2]
                                feedBytes = feedBytes[b+2:]
                                frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                                break
                        #ret, frame = video_capture.read()
                        ret = 1
                        DashComm.print("Frame Created")
                        if i < 99990: 
                            DashComm.print("Good Frame")
                            #cv2.imwrite("/home/lvuser/test.png", frame);
                            DashComm.print("Write Scucess")
                            #process ret
                            hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
                            cv2.imwrite("/home/lvuser/test.png", hsv);
                            #lower_bound = np.array([70,115,226])
                            #upper_bound = np.array([112,225,255])
                            lower_bound = np.array([73,115,226])
                            upper_bound = np.array([225,225,255])
                        
                            # Threshold the HSV image to get only green colors
                            mask = cv2.inRange(hsv, lower_bound, upper_bound)
                            #erode
                            kernel = np.ones((2,2),np.uint8)
                            erosion = cv2.erode(mask,kernel,iterations = 1)
                            #dilate
                            dilate = cv2.dilate(erosion,kernel,iterations = 4)
                            #contour filtering
                            image, contours, hierarchy = cv2.findContours(dilate,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                            
                            if len(contours) < 1:
                                self.cvWorking = False
                                DashComm.print("No Targets Found")
                            else:
                                DashComm.print("Targets Found")
                                contourMax = 0
                                contourMaxPerimeter = 0
                                contourX = 0
                                contourY = 0
                                for contour in contours:
                                    M = cv2.moments(contour)
                                    cx = int(M['m10']/M['m00'])
                                    cy = int(M['m01']/M['m00'])
                                    area = cv2.contourArea(contour)
                                    perimeter = cv2.arcLength(contour,True)
                                    if perimeter > contourMaxPerimeter:
                                        contourMax = contour
                                        contourMaxPerimeter = perimeter
                                        contourX = cx
                                        contourY = cy
                                        
                                wpilib.SmartDashboard.putNumber("CUSTOM Largest x", contourX)
                                wpilib.SmartDashboard.putNumber("CUSTOM Largest y", contourY)
                                wpilib.SmartDashboard.putNumber("CUSTOM X Error", self.center_x - contourX)
                                wpilib.SmartDashboard.putNumber("CUSTOM Rotate Error", self.degrees_per_x_error * (self.center_x - contourX))
                                wpilib.SmartDashboard.putNumber("CUSTOM Y Error", self.center_y - contourY)
                                
                                self.rotateError = self.degrees_per_x_error * (self.center_x - contourX)
                                self.y = contourY
                                self.cvWorking = True
                            import time
                            time.sleep(0.2)
                        else:
                            self.cvWorking = False
                            continue
                    
                import time
                time.sleep(2)
            except :
                import time
                time.sleep(2)
    def __init__(self):
        '''
        Constructor
        '''
        #start GRIP
        #gb_thread.start_new_thread( self.startProcess, ("Grip-Thread", "literally nothing",))
        self.cvWorking = False
        self.rotateError = 0
        self.largestArea = 0
        self.largestIndex = -1
        #print("Setting IP Address...")
        #print("Getting Table...")
        self.table = NetworkTable.getTable("/GRIP/targetDetection")
        #print("Done!")