from ServerConfig import * 
from threading import Thread
from socket import * 

import pickle

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
                self.sendAddress(addr)
                 
        self.removeAllClients()
        self.server.close()
 
    def receive(self, addr, client):
        while True:            
            try:
                recv = client.recv(1024)                
            except Exception as e:
                print('Recv() Error :', e)                
                break
            else:
                for c in self.clients:
                    if(c.getpeername() == client.getpeername()):
                        c.send(recv)
                        
               
 
         
        self.removeClient(addr, client)
    
    def sendAddress(self, senderAddr):
        try:
            for c in self.clients:
                print(c.getsockname())
                print(c.getpeername())
                print(senderAddr)
                c.send(pickle.dumps(senderAddr))

                #if(c.getpeername() == senderAddr):
                #    c.send(pickle.dumps(senderAddr))
                #    print("Send to :", senderAddr)
                
        except Exception as e:
            print("Send Address() Error : ", e) 

    def send(self, msg, senderAddr):
        try:
            if senderAddr == 1:
                for c in self.clients:
                    c.send(msg.encode())    
            else:
                for c in self.clients:
                    if(c.raddr != senderAddr):
                        c.send(msg.encode())
        except Exception as e:
            print('Send() Error : ', e)
 
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