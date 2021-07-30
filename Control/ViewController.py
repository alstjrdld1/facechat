from View.ChatRoomWindow import ChatRoom
from View.ChatListRoom import ChatListPage
from View.MyPage import MyPage
from View.AlertBox import AlertBox
from View.UserRoomPage import UserRoomPage
from View.Page import Page
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from myconfig import *
from View.Login import LoginPage
from View.InitPage import InitPage
from View.FindPWPage import FindPWPage
from View.FindIDPage import FindIDPage
from View.SignUpPage import SignUpPage
from Control.SingleTon import * 

class ViewController(SingletonInstane):
    mainWindow = None 

    def __init__(self):
        self.pageHistory = []

    def registerMainWindow(self, window):
        self.mainWindow = window
        self.mainWindow.setCentralWidget(InitPage())

    def changePage(self, pageName):
        self.pageHistory.append(self.mainWindow.takeCentralWidget()) 

        # LOGIN PAGE 가는거 
        if(pageName == LOGIN):
            self.mainWindow.setCentralWidget(LoginPage())

        # FIND ID PAGE 가는거
        elif(pageName == FIND_ID):
            self.mainWindow.setCentralWidget(FindIDPage())

        # FIND PW PAGE 가는거
        elif(pageName == FIND_PW):
            self.mainWindow.setCentralWidget(FindPWPage())

        # SIGN UP PAGE 가는거
        elif(pageName == SIGN_UP):
            self.mainWindow.setCentralWidget(SignUpPage())

        # 채팅하기, 내정보 관리, 로그아웃 선택하는 PAGE 가는거
        elif(pageName == USER_ROOM):
            self.mainWindow.setCentralWidget(UserRoomPage())
        
        elif(pageName == CHAT_LIST):
            self.mainWindow.setCentralWidget(ChatListPage())

        # MY PAGE 가는거
        elif(pageName == MY_PAGE):
            self.mainWindow.setCentralWidget(MyPage())

        # LOGOUT
        elif(pageName == LOGOUT):
            self.pageHistory.clear()
            self.mainWindow.setCentralWidget(InitPage())

        elif(pageName == CHAT_ROOM):
            chatWindow = ChatRoom()
            chatWindow.show()
            self.pageHistory.pop()            
        else:
            err = AlertBox("Error", "Call Wrong page")
            err.exec_()
        print(self.pageHistory)
    
    def goBack(self):
        prevPage = self.pageHistory.pop()
        print(prevPage)
        self.mainWindow.setCentralWidget(prevPage)
        print("Back Button worked!")