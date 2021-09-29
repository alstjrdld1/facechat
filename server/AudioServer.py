from ServerConfig import * 
from threading import Thread

class AudioServer:
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
            self.server.bind((ip, port))
        except Exception as e:
            print("Audio Server Bind Error : ", e)
            return False
        else:
            self.bListen = True
            self.t = Thread(target = self.listen, args=(self.server, ))
            self.t.start()
            print("Audio Server Listening... ")
        
        return True
    
    def stop(self):
        self.bListen = False
        if hasattr(self, 'server'):
            self.server.close()
            print("Audio Server Stop")
    
    def listen(self, server):
        while self.bListen:
            server.listen(5)
            try:
                client, addr = server.accept()
            except Exception as e :
                print("Audio Server Accept() Error : ", e)
                break
            else:
                print(client)
                self.clients.append(client)
                self.ip.append(addr)
                t = Thread(target = self.receive, args=(addr, client))
                self.threads.append(t)
                t.start()

        self.removeAllClients()
        self.server.close()

    def receive(self, addr, client):
        while True:    
            try:
                data = client.recv(1024)
                self.broadcast(client, data)
            
            except Exception as e :
                print("Audio Server Receive Error on : ", client)
                print("Reason : ", e)
                self.removeClient(addr, client)
                client.close()

    def removeClient(self, addr, client):
        # find closed client index
        idx = -1
        for k, v in enumerate(self.clients):
            if v == client:
                idx = k
                break
 
        client.close()
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
        
    def broadcast(self, sock, data):
        for client in self.clients:
            if client != sock:
                try:
                    client.send(data)
                    print("Sending...")
                    print("\n Sending Audio Data : ", data)
                except:
                    pass

server = AudioServer()
server.start(SERVER_IP, AUDIO_CHAT_PORT)