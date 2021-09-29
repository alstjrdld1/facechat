import pickle
import threading
from ServerConfig import * 
from threading import Lock, Thread
from socket import * 

import numpy as np
import struct

frameList = [] 

class VideoServerSocket:
    
    def __init__(self):        
        self.bListen = False       
        self.clients = []
        self.ip = []
        self.threads = []
        self.lock = threading.Lock()

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
            self.s = Thread(target=self.send, args=())
            self.s.start()
            print("server sending start.. ")
 
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

                t = Thread(target=self.receive, args=(addr, client, ))
                self.threads.append(t)
                t.start()

        self.removeAllClients()
        self.server.close()

    def receive(self, addr, client):
        global frameList
        
        self.lock.acquire() ### Thread Lock

        frameList.append([])
        num = len(frameList) - 1
        # print("Frame List Length : ", len(frameList))

        self.lock.release() ### Thread Lock release

        data = b""
        payload_size = struct.calcsize('>L') # payload 사이즈를 측정한다. 

        # print("\n PAY LOAD SIZE : ", payload_size)
        try:
            while True:

                while len(data) < payload_size: # data에 payload가 없으면 
                    recv = client.recv(4096) # 수신을 한다. 
                    
                    # print("\n CLIENT  :", client)
                    # print("\n RECEIVED DATA LENGTH : ", len(recv))
                    
                    data += recv # 수신한 데이터를 data에 넣어준다. 

                packed_msg_size = data[:payload_size] # 메시지의 크기 (수신할 frame)의 크기를 payload int가 갖고 있어서 그만큼만 가져온다. 
                data = data[payload_size:] # payload를 제외한 뒷 내용(frame)을 data에 저장한다. 

                msg_size = struct.unpack(">L", packed_msg_size)[0] # payload할당한 만큼 4byte를 열어서 메시지의 크기(frame의 크기)를 확인한다. 

                while len(data) < msg_size: # 데이터가 메시지의 크기만큼 들어오지 않으면 
                    data += client.recv(4096) # 데이터가 메시지 크기만큼 들어올 때 까지 기다려준다. 
                    # print("Waiting msg data ....")
                 
                frame_data = data[:msg_size] # 메시지 사이즈 만큼 frame data를 추출 
                data = data[msg_size:] # 필요한 부분만 뽑아내기 

                self.lock.acquire() # Thread lock 걸기 
                # print("\n Thread lock for append frame")
                frameList[num].append(frame_data) # 가져온 frame을 FrameList에 추가 
                self.lock.release() # Thread lock 해제 
                # print("\n Thread lock release after append frame list ")

        except Exception as e : 
            print("Error : ", e)

    def send(self):
        global frameList
        idx = 0 

        while True:
            self.lock.acquire() # Thread lock 실행 
            # print("\n Thread Lock activate for sending frame")
            try:
                frame = None

                if len(frameList) != 0 :
                    if len(frameList[idx]) == 0:
                        
                        self.lock.release()
                        continue
                    frame = frameList[idx].pop(0) # Frame List에 프레임이 들어와 있으면 dequeue 진행 

                else:
                    self.lock.release() # Error 방지로 frameLis 비어있으면 thread lock 해제하고 다시 while문 돌림 
                    # print("\n Thread Lock release because no frame list")
                    continue
                
                size = len(frame) # 현재 갖고 있는 frame의 사이즈 측정
                willsend = struct.pack('>L', size) + frame # client가 송신하는 것 처럼 data 사이즈를 packing해서 frame과 결합

                for index, c in enumerate(self.clients):
                    # print("current sending client index : ", index)
                    c.sendall(willsend) # 전송                 
                    # if index == idx :
                    #     continue
                idx += 1
                
                if idx == len(frameList):
                    idx = 0

                self.lock.release() # Thread lock 해제 
                # print("\n Thread lock release because send success")

            except Exception as e :
                print("\n Server Send Error on Frame List : ", e)
                pass

    def removeClient(self, addr, client):
        # find closed client index
        global frameList
        idx = -1
        for k, v in enumerate(self.clients):
            if v == client:
                idx = k
                break
 
        client.close()
        self.ip.remove(addr)
        self.clients.remove(client)
        frameList.pop(idx)
 
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