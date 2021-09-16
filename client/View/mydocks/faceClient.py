from threading import *
from socket import *
import pickle
import struct
import time
import cv2
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
            
    ### 가장 간단한 폼 
    # def receive(self, client):
    #     while self.bConnect:            
    #         try:
    #             data = client.recv(921600)             

    #             #print("RECEIVED DATA TYPE : ", type(data))
                
    #             if(len(data) == 921600):
    #                 frame = np.fromstring(data, dtype=np.uint8)

    #                 frame = frame.reshape(480, 640, 3)
    #                 self.recv.recv_signal.emit(frame)
    #             else:
    #                 print("FAIL, RECEIVED DATA LENGTH IS : ", len(data))

    #         except Exception as e:
    #             print('Recv() Error :', e)                 
    #             break 

    #     self.stop() 

    # ### 느리게 되는 거 
    # def receive(self, client):
    #     frame = b""

    #     while self.bConnect:
    #         try:
    #             ### data 받는 곳 
    #             data = client.recv(921600)

    #             # print("\n RECIEVED DATA LENGTH : ", len(data))
    #             # print("\n RECEIVED DATA TYPE : ", type(data))
    #             # print("\n Current frame LENGTH : ", len(frame))
    #             # print("\n Current frame type : ", type(frame))

    #             frame += data 

    #         except Exception as e :
    #             print('Recv() error : ', e)
    #             break

    #         ### video 포맷팅     
    #         try:
    #             if(len(frame) >= 921600):
    #                 video = np.fromstring(frame[:921600], dtype=np.uint8)
    #                 video = video.reshape(480, 640, 3)
    #                 self.recv.recv_signal.emit(video)
    #                 frame = frame[921600:]

    #         except Exception as e :
    #             print("\n video reshaping error : ", e)            

    def receive(self, client):
        payload_size = struct.calcsize('>L')
        print("PAY LOAD SIZE : ", payload_size )
        data = b""

        while self.bConnect:
            try:
                break_loop = False

                while len(data) < payload_size:
                    received = client.recv(4096)
                    # print("\n RECEIVED DATA : ", received) 
                    if received == b'':
                        client.close()
                        break_loop = True
                        break
                    data += received

                packed_msg_size = data[:payload_size]
                data = data[payload_size:]

                msg_size = struct.unpack(">L", packed_msg_size)[0]

                # print("\n RECEIVED MSG_SIZE : ", msg_size)
                # print("\n CURRENT DATA SIZE : ", len(data))

                while len(data) < msg_size:
                    data += client.recv(4096)


                frame_data = data[:msg_size]
                data = data[msg_size:]

                frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
                # print("FRAME : ", frame)
                # print("\n Frame shape : ", frame.shape)
                frame = cv2.imdecode(frame[1] ,cv2.IMREAD_COLOR)
                self.recv.recv_signal.emit(frame)
                
            except Exception as e :
                print("\n Receive Error : ", e)

        client.close()

    # def send(self, msg):
    #     if not self.bConnect: 
    #         print("\n CONNECTION ERROR ")
    #         return
    #     try:         
    #         message = msg.flatten()
    #         #print("SENDING MESSAGE DATA TYPE : ", type(message))
    #         #print("SENDING MESSAGE DATA LEN : " , len(message))
    #         video = message.tostring()
    #         # print("SENDING DATA LENGTH : ", len(video))
    #         self.client.sendall(video)
    #         # print("SEND : ", video)
    #     except Exception as e:
    #         print('Send() Error : ', e)
    #     else:
    #         return

    def send(self, msg):
        if not self.bConnect: 
            print("\n CONNECTION ERROR ")
            return
        try:         
            video = cv2.imencode('.jpg', msg, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
            # print("\n msg type : {}, video type : {}".format(type(msg), type(video)))
            # print("\n sending video : ", video)
            # print("\n msg shape : ", msg.shape)
            # print("\n msg length : ", len(msg))
            # print("\n video shape : {}, {}".format(video[0], len(video[1])))

            data = pickle.dumps(video ,0)
            size = len(data)
            # print("\n sending data size : ", size)

            try:
                willsend = struct.pack('>L', size) + data
                # print("\n WILL SEND : ", willsend)
                # print("\n will send data length : ", len(willsend))
                self.client.sendall(willsend)

            except Exception as e :
                print("\n sending error : ", e)

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
        