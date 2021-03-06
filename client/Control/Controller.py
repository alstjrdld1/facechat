from View.dialogs.AlertBox import AlertBox
from Control.DatabaseController import DatabaseController
from Model.User import User
from face_recognition.faceID import FaceID
from Control.SingleTon import * 
from os import listdir
from os.path import isfile, join
import threading

current_user_count = 1

class Controller(SingletonInstane):
    
    currentUser = None 
    chatRoomUser = 1
    lock = threading.Lock()

    def __init__(self):
        from Control.ViewController import ViewController
        self.dbConn = DatabaseController()
        self.vc = ViewController()
        super().__init__()
        
    def printHello(self):
        print("Hello")
    
    def textLogin(self, Id, Pw):
        result = self.dbConn.instance().pwCheck(Id, Pw)
        print(result)
        if(result != None):
            self.currentUser = User(result[0],result[1],result[2],result[3],result[4],result[5],result[6])
            return True
        else:
            return False

    def faceLogin(self):
        loginSuccess = FaceID().login()
        for i in range(2):
            if loginSuccess: 
                # face 디렉토리에서 이름 파싱해서 가져오기 
                path = 'client/face_recognition/faces/'
                file_list = listdir(path)
                self.currentUser = self.getUser(file_list[0][:file_list[0].find('_')])
                break
            else : 
                loginSuccess = FaceID().login()
        return loginSuccess
    
    def faceRegister(self):
        print(self.currentUser.getId())
        FaceID().register(self.currentUser.getId())

    def getId(self, PhNum, Name):
        auth = self.dbConn.instance().get_name_id_phNum(PhNum, Name)
        return auth
    
    def getPassword(self, Id, PhNum, Name):
        auth = self.dbConn.instance().get_pw(Id, PhNum, Name)
        return auth

    def getCurrentUser(self):
        return self.currentUser

    def changeUserInfo(self, Name, PhNum, Email, NickName, Id, Pw, Greeting):

        success = self.dbConn.instance().changeInfo(Name, PhNum, Email, NickName, Id, Pw, Greeting)
        if success :
            self.currentUser.setUser(Name, PhNum, Email, NickName, Id, Pw, Greeting)
            msg = AlertBox("CHAGNE INFO", "CHANGED!")
            msg.exec_()
            self.vc.instance().goBack()
        else :
            msg = AlertBox("CHAGNE INFO", "FAIL!")
            msg.exec_()

    
    def signIn(self, id, pw):
        result = self.dbConn.instance().pwCheck(id ,pw)
        
        if(result != None):
            self.currentUser = User(result[0],result[1],result[2],result[3],result[4],result[5],result[6])
        
        return result

    def signUp(self, Name, PhNum, Email, NickName, Id, Pw, Greeting):
        user = None
        
        if(self.dbConn.instance().insertUser(Name, PhNum, Email, NickName, Id, Pw, Greeting) != None):
            user = User(Name, PhNum, Email, NickName, Id, Pw, Greeting)
            print(user)
            self.currentUser = user
            return True

        return False
    
    def getUser(self, id):
        result = self.dbConn.instance().loadUser_id(id)
        if len(result) != 0 : 
            return User(result[0],result[1],result[2],result[3],result[4],result[5],result[6])
        else:
            return None 
    
    def getChatRoomUserNumber(self):
        return self.chatRoomUser

    def setChatRoomUserNumber(self, num):
        global current_user_count

        if num == 1:
            return

        self.chatRoomUser = num         

        self.lock.acquire()
        if(current_user_count != self.chatRoomUser):
            current_user_count = self.chatRoomUser 
        self.lock.release()
