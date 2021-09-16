from threading import *
from socket import *
from PyQt5.QtCore import Qt, pyqtSignal, QObject
 
class Signal(QObject):  
    recv_signal = pyqtSignal(str)
    disconn_signal = pyqtSignal()   
 
class ClientSocket:
 
    def __init__(self, parent):        

        from Control.Controller import Controller

        self.controller = Controller()
        self.parent = parent                
        
        self.recv = Signal()        
        self.recv.recv_signal.connect(self.parent.updateMsg)
        self.disconn = Signal()        
        self.disconn.disconn_signal.connect(self.parent.updateDisconnect) 
 
        self.bConnect = False
         
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
            self.disconn.disconn_signal.emit()
 
    def receive(self, client):
        while self.bConnect:            
            try:
                recv = client.recv(1024)                
            except Exception as e:
                print('Recv() Error :', e)                
                break
            else:                
                msg = str(recv, encoding='utf-8')
                if msg:
                    if msg.find("[관리자]") == 0:
                        self.clientNumberUpdate(msg)
                        print("관리자 키워드 찾음")
                        continue
                    self.recv.recv_signal.emit(msg)
                    print('[RECV]:', msg)
 
        self.stop()

    def clientNumberUpdate(self, msg):
        if(msg[:5] != "[관리자]"):
            return False
        headIdx = msg.find("은")
        tailIdx = msg.find("명")

        people = int(msg[headIdx + 1 : tailIdx])
        self.controller.instance().setChatRoomUserNumber(people)

    def send(self, msg):
        if not self.bConnect:
            return
 
        try:            
            msg = "[" + self.controller.instance().getCurrentUser().getNickName() + "] " + msg
            self.client.send(msg.encode())
        except Exception as e:
            print('Send() Error : ', e)