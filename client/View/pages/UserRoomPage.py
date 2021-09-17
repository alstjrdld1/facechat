from View.ChatRoomWindow import ChatRoom
from PyQt5.QtWidgets import QPushButton
from View.pages.Page import Page

from myconfig import *

class UserRoomPage(Page):
    def __init__(self):
        from Control.ViewController import ViewController
        from Control.Controller import Controller
        self.controller = Controller()
        self.vc = ViewController()
        super().__init__()
        self.setupUI()
    
    def setupUI(self):
        self.pageName.setText("WAITING ROOM")

        self.startChatBtn = QPushButton("START CHAT")
        self.startChatBtn.clicked.connect(self.clickStartChat)

        self.editInfoBtn = QPushButton("MY PAGE")
        self.editInfoBtn.clicked.connect(self.clickEditInfo)

        self.faceIDBtn = QPushButton("FACE ID REGISTER")
        self.faceIDBtn.clicked.connect(self.faceIDBtnClick)

        self.logoutBtn = QPushButton("LOGOUT")
        self.logoutBtn.clicked.connect(self.clickLogout)

        self.pageLayout.addWidget(self.startChatBtn, 1, 0)
        self.pageLayout.addWidget(self.editInfoBtn, 2, 0)
        self.pageLayout.addWidget(self.faceIDBtn, 3, 0)
        self.pageLayout.addWidget(self.logoutBtn, 4, 0)


        self.setLayout(self.pageLayout)

    def clickStartChat(self):
        self.chatroom = ChatRoom(self)
        self.chatroom.show()
        self.vc.instance().registerChatWindow(self)
        # self.vc.instance().changePage(CHAT_ROOM)
    
    def clickEditInfo(self):
        self.vc.instance().changePage(MY_PAGE)
    
    def clickLogout(self):
        self.controller.instance().currentUser = None
        self.vc.instance().changePage(LOGOUT)
    
    def faceIDBtnClick(self):
        self.controller.instance().faceRegister()