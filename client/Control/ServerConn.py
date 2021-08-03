import socket 

class ServerConn:
    def __init__(self):
        self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    

    def connect(self):
        pass