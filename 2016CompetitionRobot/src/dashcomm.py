'''
Created on Mar 6, 2016

@author: illid_000
'''

import socket
import _thread
import wpilib
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

    def server_thread_run(self, som,thingy):
        print("Server Thread RUn")
        
        print("Temp ping")
        import os
        hostname = ""
        while 1:
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    self.socket.bind((self.TCP_IP, self.TCP_PORT))
                    self.socket.listen(5)
                    self.socket.settimeout(5)
                    while 1:
                        print("Socket Listen")
                        conn, addr = self.socket.accept()
                        print("Socket Accepted")
                        while conn and addr:
                            print("Socket Valid")
                            t,d,p = 0,0,0
                            self.acc_data_lock.acquire()
                            t = self.curr_type
                            d = self.curr_defense
                            p = self.curr_position
                            self.acc_data_lock.release()
                            #self.socket.se
                            conn.send(bytes('c' + chr(t) + chr(d) + chr(p), 'ASCII'))
                            conn.settimeout(3)
                            data = conn.recv(self.BUFFER_SIZE)
                            if not data: return
                            print("Data Valid: {} {} {} {}".format(data[0], data[1], data[2], data[3]))
                except:
                    self.socket.close()
            except:
                pass
                    
        wpilib.Timer.delay(3)
            

        print("Server THread Termintaed")
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
        self.curr_type = 5
        self.curr_defense = 13
        self.curr_position = 27
        
        
        _thread.start_new_thread( self.server_thread_run, ("Dashboard-Comm-Thread", "literally nothing",))