import myconfig 

import socket

class Query:
    __conn = 1
    def sendQuery(str):
        tmp = __conn

class ServerConn: 
    def __init__(self):
        # Here to make socket connection between local program and server 
        sio = socket.Client()

    # This port is for login with id and pw 
    def to5000(self, id, pw):
        # if user is exist 

        return False 

    # This port is for send frame 
    def to5001(self, frame):
        # if this frame is registered in db, send true or user data 

        return False 
