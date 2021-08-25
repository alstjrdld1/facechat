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

                #print("RECEIVED DATA TYPE : ", type(data))
                
                if(len(data) == 921600):
                    frame = np.fromstring(data, dtype=np.uint8)

                    frame = frame.reshape(480, 640, 3)
                    self.recv.recv_signal.emit(frame)
                else:
                    print("FAIL, RECEIVED DATA LENGTH IS : ", len(data))

            except Exception as e:
                print('Recv() Error :', e)                 
                break 

        self.stop() 

    # def receive(self, client):
    #     frame = b""

    #     while self.bConnect:
    #         try:
    #             ### data 받는 곳 
    #             data = client.recv(921600)
    #             print("\n RECIEVED DATA LENGTH : ", len(data))
    #             print("\n RECEIVED DATA TYPE : ", type(data))
    #             print("\n Current frame LENGTH : ", len(frame))
    #             print("\n Current frame type : ", type(frame))

    #             ### frame 크기 안 모이면 다시 while 루프 
    #             if(len(frame) < 921600):
    #                 frame += data 
    #                 print("\n Receive function called ")
    #                 continue 
                
    #         except Exception as e :
    #             print('Recv() error : ', e)
    #             break

    #         ### video 포맷팅     
    #         try:
    #             video = np.fromstring(frame, dtype=np.int8)
    #             video = video.reshape(480, 640, 3)
    #             frame = frame[921600:]
    #             self.recv.recv_signal.emit(video)

    #         except Exception as e :
    #             print("\n video reshaping error : ", e)            


    # def receive(self, client):
    #     data = b""
    #     metadata_size = struct.calcsize("Q")

    #     while True:
    #         try : 
    #             while len(data) < metadata_size : 
    #                 packet = client.recv(4 * 1024)  
    #                 # packet = client.recv(921600) 
    #                 if not packet: break
    #                 data += packet
    #             packed_msg_size = data[:metadata_size]
    #             data = data[metadata_size:]
    #             msg_size = struct.unpack("Q", packed_msg_size)[0]

    #         except Exception as e :
    #             print("\n Error on receive first while 1 : ", e)
    #             break

    #         try : 

    #             while len(data) < msg_size : 
    #                 data += client.recv(4 * 1024) 
    #                 # data += client.recv(921600)
    #                 frame_data = data[:msg_size]
    #                 data = data[msg_size:]
    #                 try :  
    #                     frame = pickle.loads(frame_data)
    #                 except Exception as e :
    #                     # print("\n data : ", data)
    #                     # print("\n frame data : ", frame_data)
    #                     # print("\n print frame : ", frame)
    #                     # print("\n frame type : ", frame)
    #                     print("\n pickle Error : ", e)
                     
    #                 try : 
    #                     self.recv.recv_signal.emit(frame)   
    #                 except Exception as e :
    #                     print("\n send signal error : ", e)
                    
    #         except Exception as e :
    #             print("\n Error on frame emit : ", e) 
    #             break
 
                
    def send(self, msg):
        if not self.bConnect: 
            print("\n CONNECTION ERROR ")
            return
        try:         
            message = msg.flatten()
            #print("SENDING MESSAGE DATA TYPE : ", type(message))
            #print("SENDING MESSAGE DATA LEN : " , len(message))
            video = message.tostring()
            # print("SENDING DATA LENGTH : ", len(video))
            self.client.sendall(video)
            # print("SEND : ", video)
        except Exception as e:
            print('Send() Error : ', e)
        else:
            return

    # def send(self, msg):
    #     if not self.bConnect:
    #         return 
    #     try: 
    #         # print("Sending this frame : ", msg)
    #         print("msg len : ", len(msg))
    #         img_serialize = pickle.dumps(msg)

    #         print("img_serialize len : ", len(img_serialize))
    #         message = struct.pack("Q", len(img_serialize)) + img_serialize 
    #         # print("\n sending frame type : ", type(img_serialize))
    #         # print("\n Sending frame : ", img_serialize)
            
    #         self.client.sendall(img_serialize)


    #     except Exception as e : 
    #         print("\n Send() Error : ", e)
        