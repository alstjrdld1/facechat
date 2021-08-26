from ServerConfig import * 
from threading import Thread
from socket import * 

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
 
    def receive(self, addr, client):
        frame = b""
        while True:            
            try:
                data = client.recv(921600) 
                # print("\n RECEIVED DATA TYPE : ", type(data))

                # time.sleep(0.02)
                # data = client.recv(4 * 1024) 

            except Exception as e:
                print('Recv() Error :', e)                
                break
            else:
                # print("DATA LEN : ", len(data))
                # print("FROM : {}, RECEIVED DATA LENGTH : {}".format(addr, len(data)))
                frame += data
                
                if(len(frame) >= 921600):
                    for c in self.clients:
                        if(c.getpeername() != client.getpeername()):
                            # print(len(data))
                            c.sendall(frame[:921600])
                    frame = frame[921600:]
                
                #  print("SEND SUCCESS ")

        self.removeClient(addr, client)
        return

    # def receive(self, addr, client):
    #     data = b""
    #     metadata_size = struct.calcsize("Q")

    #     while True:
    #         ### receive meta data 
    #         try : 
    #             while len(data) < metadata_size : 
    #                 # packet = client.recv(4 * 1024)  
    #                 packet = client.recv(921600)
    #                 if not packet: break
    #                 data += packet
    #             packed_msg_size = data[:metadata_size]
    #             data = data[metadata_size:]
    #             msg_size = struct.unpack("Q", packed_msg_size)[0]

    #         except Exception as e :
    #             print("Error on receive first while 1 : ", e)
    #             break

    #         ### make frame_data
    #         try : 
    #             while len(data) < msg_size : 
    #                 try :
    #                     data += client.recv(921600)
    #                     # data += client.recv(4 * 1024) 
    #                 except Exception as e :
    #                     print("data receive error : ", e)

    #                 frame_data = data[:msg_size]
    #                 data = data[msg_size:]

    #                 try : 

    #                     frame = pickle.loads(frame_data)
    #                 except Exception as e :
    #                     print("pickle load error : ", e)
                        
                    
    #         except Exception as e :
    #             print("Error on frame : ", e) 
    #             break
            
    #         ### send frame
    #         try :
    #             serialized_frame  = self.serialize(frame)
                
    #             for c in self.clients:
    #                 if(c.getpeername() == client.getpeername()):
    #                     c.sendall(serialized_frame)

    #         except Exception as e : 
    #             print("Serialize error and sending error : ", e)
    #             break

    def serialize(self, msg):
        try: 
            img_serialize = pickle.dumps(msg)
            message = struct.pack("Q", len(img_serialize)) + img_serialize 

        except Exception as e : 
            print("Send() Error : ", e)
        
        else:
            return message

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