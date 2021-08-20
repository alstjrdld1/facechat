from ServerConnector import *

class Authenticate:

    def idpwLogin(self, id, pw):
        # Send query that id is exist 
        currentUser = Query.sendquery('')

        # Query exist means user is exist 
        if currentUser:
            if(pw == currentUser.pw):
                return currentUser
        
        else : 
            return False

    def faceIDLogin(self, frame):
        # send to server 
        currentUser = ServerConn.to5000(frame)