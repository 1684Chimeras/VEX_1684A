'''
Created on Mar 6, 2016

@author: illid_000
'''

import socket
import _thread
import wpilib
import select
from threading import Lock
  
#Communicates with thee auton thingh
class DashComm(object):
    '''
    classdocs
    '''
    TCP_IP = '' #localhost
    TCP_PORT = 5805 #one of the designated communications ports
    BUFFER_SIZE = 1024 #its 3 bytes
    
    acc_data_lock = Lock()

    curr_type = 0
    curr_defense = 0
    curr_position = 0

    @staticmethod
    def isFMSAttached():
        return wpilib.DriverStation.isFMSAttached(wpilib.DriverStation.getInstance())
    
    @staticmethod
    def log(str):
        pass
    
    @staticmethod
    def print(str):
        if DashComm.isFMSAttached():
            DashComm.log(str)
        else:
            print(str)
            
    @staticmethod
    def getNumber(key,default):
        if not DashComm.isFMSAttached():
            return wpilib.SmartDashboard.getNumber(key,default)
        else:
            return default
        
    @staticmethod
    def putNumber(key,default):
        if not DashComm.isFMSAttached():
            wpilib.SmartDashboard.putNumber(key,default)
        else:
            pass
    
    def getMode(self):    
        return self.curr_type
    
    def getPosition(self):
        return self.curr_position
    
    def getDefense(self):
        return self.curr_defense
    
    def clear(self):
        self.dataValid = False
        self.curr_defense = 0
        self.curr_position = 0
        self.curr_type
    
    def validData(self):
        return self.dataValid and self.curr_defense != 0 and self.curr_position != 0 and self.curr_type != 0
     
    def processData(self, data):
        if data[1] != 0:
            self.curr_type = data[1]
        if data[2] != 0:
            self.curr_defense = data[2]
        if data[3] != 0:
            self.curr_position = data[3]
        
    
    def server_thread_run(self, som,thingy):
        DashComm.print("[DashComm] Starting Server Thread")
        
        import os
        import time
        self.clear()
        while 1:
            self.clear()
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                DashComm.print("[DashComm] Attempting to obtain socket 5805...")
                self.socket.bind((self.TCP_IP, self.TCP_PORT))
                self.socket.settimeout(5)
                self.socket.listen(0)
                DashComm.print("[DashComm] Successfully obtained socket 5805!")
                try:
                    while 1:
                        self.dataValid = False
                        DashComm.print("[DashComm] Listening for a connection. . .")
                        conn, addr = self.socket.accept()
                        DashComm.print("[DashComm] Found a connection!")
                        while conn and addr:
                          #  DashComm.print("[DashComm] The connection is valid!")
                            conn.settimeout(3)
                            conn.send(bytes('c' + chr(self.curr_type) + chr(self.curr_defense) + chr(self.curr_position), 'ASCII'))
                            data = conn.recv(self.BUFFER_SIZE)
                          #  DashComm.print("Data Valid: {} {} {} {}".format(data[0], data[1], data[2], data[3]))
                            self.processData(data)
                            self.dataValid = True 
                except Exception as ex:
                    self.dataValid = False
                    DashComm.print("[DashComm] Goodbye.")
                    conn.close()
                    self.socket.close()
                    time.sleep(2)
            except:
                wpilib.DriverStation.reportError("RESTART THE ROBORIO IF YOU WANT TO USE DS AUTON!!!! SOCKET 5805 OCCUPIED", False)
                #print("Exception : " + ex)
                self.dataValid = False
            finally:
                self.socket.close()
                time.sleep(5)
            

        DashComm.print("Server THread Termintaed")
    def update_sock_data(self, selectedType, selectedDefense, selectedPosition):
        self.acc_data_lock.acquire()
        self.curr_type = selectedType
        self.curr_defense = selectedDefense
        self.curr_position= selectedPosition
        self.acc_data_lock.release()
        
    def __init__(self):
        '''
        Constructor
        '''
        print("DashComm Init")
        self.curr_type = 0
        self.curr_defense = 0
        self.curr_position = 0
        self.dataValid = False
        
        
        _thread.start_new_thread( self.server_thread_run, ("Dashboard-Comm-Thread", "literally nothing",))