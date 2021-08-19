from threading import *
from socket import *
import pickle
import struct
import time
from PyQt5.QtCore import Qt, pyqtSignal, QObject

import numpy as np
class Signal(QObject):  
    recv_signal = pyqtSignal(np.ndarray)
 
class FaceClientSocket:
    peer = None 
    def __init__(self, parent):        
        self.parent = parent                

        self.recv = Signal()

        self.bConnect = False
        self.targetAddress = ""
         
    def __del__(self):
        
        self.stop()
 
    def connectServer(self, ip, port):
        self.client = socket(AF_INET, SOCK_STREAM)           
 
        try:
            self.client.connect( (ip, port) )
        except Exception as e:
            print('Connect Error : ', e)
            return False
        else:
            self.bConnect = True
            self.t = Thread(target=self.receive, args=(self.client,))
            self.t.start()
            print('Connected')  
        return True
 
    def stop(self):
        self.bConnect = False       
        if hasattr(self, 'client'):            
            self.client.close()
            del(self.client)
            print('Client Stop') 
            
 
    def receive(self, client):
        while self.bConnect:            
            try:
                data = client.recv(921600)                

            except Exception as e:
                print('Recv() Error :', e)                 
                break
            else:
                #print("RECEIVED DATA TYPE : ", type(data))
                frame = np.fromstring(data, dtype=np.uint8)
                frame = frame.reshape(480, 640, 3)
                self.recv.recv_signal.emit(frame)

        self.stop()
 
    def send(self, msg):
        if not self.bConnect: 
            return
        try:         
            message = msg.flatten()
            #print("SENDING MESSAGE DATA TYPE : ", type(message))
            #print("SENDING MESSAGE DATA LEN : " , len(message))
            video = message.tostring()
            #print("SENDING DATA TYPE : ", type(video))
            #print("SENDING DATA LENGTH : ", len(video))
            self.client.sendall(video)
            # print("SEND : ", video)
        except Exception as e:
            print('Send() Error : ', e)
        else:
            return