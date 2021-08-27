from ServerConfig import * 
from threading import Thread
from socket import * 

import cv2
import numpy as np
import time
import pickle 
import struct

class VideoServerSocket:
 
    def __init__(self):        
        self.bListen = False       
        self.clients = []
        self.ip = []
        self.threads = []
         
    def __del__(self):
        self.stop()
 
    def start(self, ip, port):
        self.server = socket(AF_INET, SOCK_STREAM)            
 
        try:
            self.server.bind( (ip, port))
        except Exception as e:
            print('Bind Error : ', e)
            return False
        else:                 
            self.bListen = True
            self.t = Thread(target=self.listen, args=(self.server,))
            self.t.start()
            print('Server Listening...')
 
        return True
 
    def stop(self):
        self.bListen = False
        if hasattr(self, 'server'):            
            self.server.close()            
            print('Server Stop')
 
    def listen(self, server):
        while self.bListen:
            server.listen(5)   
            try:
                client, addr = server.accept()
            except Exception as e:
                print('Accept() Error : ', e)
                break
            else:            
                print(client)    
                self.clients.append(client)
                self.ip.append(addr)                
                t = Thread(target=self.receive, args=(addr, client))
                self.threads.append(t)
                t.start()
                 
        self.removeAllClients()
        self.server.close()

    # ### 이거 열면 느린거 
    # def receive(self, addr, client):
    #     frame = b""
    #     while True:            
    #         try:
    #             data = client.recv(921600) 
    #             # print("\n RECEIVED DATA TYPE : ", type(data))

    #             # time.sleep(0.02)
    #             # data = client.recv(4 * 1024) 

    #         except Exception as e:
    #             print('Recv() Error :', e)                
    #             break
    #         else:
    #             # print("DATA LEN : ", len(data))
    #             # print("FROM : {}, RECEIVED DATA LENGTH : {}".format(addr, len(data)))
    #             frame += data
                
    #             if(len(frame) >= 921600):
    #                 for c in self.clients:
    #                     if(c.getpeername() != client.getpeername()):
    #                         # print(len(data))
    #                         c.sendall(frame[:921600])
    #                 frame = frame[921600:]
                
    #             #  print("SEND SUCCESS ")

    #     self.removeClient(addr, client)
    #     return

    def receive(self, addr, client):
        data = b""
        payload_size = struct.calcsize('>L')
        print("\n PAY LOAD SIZE : ", payload_size)
        count = 0 
        while True:
            count = count + 1
            print("\n while loop count : ", count)
            while len(data) < payload_size:
                recv = client.recv(4096)
                print("\n RECEIVED DATA LENGTH : ", len(recv))

                data += recv 
            
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]

            msg_size = struct.unpack('>L', packed_msg_size)[0]

            print("\n RECEIVED MSG_SIZE : ", msg_size)
            print("\n CURRENT DATA SIZE : ", len(data))

            while len(data) < msg_size:
                data += client.recv(4096)
            
            frame_data = data[:msg_size]
            data = data[msg_size:]
            print("\n FRAME DATA LENGTH : ", len(frame_data))
            print("\n REST OF DATA LENGTH  :", len(data))
            
            for c in self.clients:
                if (c.getpeername() == client.getpeername()):
                    c.sendall(frame_data)

            # frame = pickle.loads(frame_data, fix_imports = True, encoding = 'bytes')
            # frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            



    def removeClient(self, addr, client):
        # find closed client index
        idx = -1
        for k, v in enumerate(self.clients):
            if v == client:
                idx = k
                break
 
        client.close()
        self.ip.remove(addr)
        self.clients.remove(client)
 
        del(self.threads[idx])
        self.resourceInfo()
 
    def removeAllClients(self):
        for c in self.clients:
            c.close()
 
        self.ip.clear()
        self.clients.clear()
        self.threads.clear()
 
        self.resourceInfo()
 
    def resourceInfo(self):
        print('Number of Client ip\t: ', len(self.ip) )
        print('Number of Client socket\t: ', len(self.clients) )
        print('Number of Client thread\t: ', len(self.threads) )

ip = gethostbyname(gethostname())

vcs = VideoServerSocket()
vcs.start(ip, FACE_CHAT_PORT)