from face_recognition.faceID import FaceID
from SingleTon import * 

class Controller(SingletonInstane):
    def __init__(self):
        super().__init__()

    def printHello(self):
        print("Hello")
    
    def textLogin(self):
        pass 

    def faceLogin(self):
        loginSuccess = FaceID().login()
        for i in range(2):
            if loginSuccess: 
                break
            else : 
                loginSuccess = self.faceLogin()

        return loginSuccess
    