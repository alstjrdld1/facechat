from PyQt5.QtWidgets import QPushButton
from View.Page import Page

from myconfig import *

class UserRoomPage(Page):
    def __init__(self):
        from Control.ViewController import ViewController
        self.vc = ViewController()
        super().__init__()
        self.setupUI()
    
    def setupUI(self):
        self.pageName.setText("WAITING ROOM")

        self.startChatBtn = QPushButton("START CHAT")
        self.startChatBtn.clicked.connect(self.clickStartChat)

        self.editInfoBtn = QPushButton("MY PAGE")
        self.editInfoBtn.clicked.connect(self.clickEditInfo)

        self.logoutBtn = QPushButton("LOGOUT")
        self.logoutBtn.clicked.connect(self.clickLogout)

        self.pageLayout.addWidget(self.startChatBtn, 1, 0)
        self.pageLayout.addWidget(self.editInfoBtn, 2, 0)
        self.pageLayout.addWidget(self.logoutBtn, 3, 0)

        self.setLayout(self.pageLayout)

    def clickStartChat(self):
        self.vc.instance().changePage(CHAT_LIST)
    
    def clickEditInfo(self):
        self.vc.instance().changePage(MY_PAGE)
    
    def clickLogout(self):
        self.vc.instance().changePage(LOGOUT)