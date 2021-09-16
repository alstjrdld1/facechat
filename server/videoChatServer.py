from ServerConfig import * 
from threading import Thread
from socket import * 

import numpy as np
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
            print('Video Server Stop')
 
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
        try:
            while True:

                while len(data) < payload_size:
                    recv = client.recv(4096)
                    print("\n CLIENT  :", client)
                    print("\n RECEIVED DATA LENGTH : ", len(recv))

                    for c in self.clients:
                        # if (c.getpeername() == client.getpeername()):
                        # print(recv)
                        c.sendall(recv)

        except Exception as e : 
            print("Error : ", e)
            
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

vcs = VideoServerSocket()
vcs.start(SERVER_IP, FACE_CHAT_PORT)