from threading import *
from socket import *
from PyQt5.QtCore import Qt, pyqtSignal, QObject

import numpy as np
class Signal(QObject):  
    recv_signal = pyqtSignal(np.ndarray)
 
class FaceClientSocket:
    peer = None 

    def __init__(self, parent):        
        self.parent = parent                

        self.recv = Signal()
        self.recv.recv_signal.connect(self.parent.update_other_image)

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
                recv = client.recv(1024)                
            except Exception as e:
                print('Recv() Error :', e)                 
                break
            else:
                if(recv):
                    self.recv.recv_signal.emit(recv)
                    print(recv)
 
        self.stop()
 
    def send(self, msg):
        if not self.bConnect: 
            return
 
        try:         
            self.client.send(msg)
        except Exception as e:
            print('Send() Error : ', e)