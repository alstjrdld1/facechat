from View.AlertBox import AlertBox
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QHBoxLayout, QLineEdit, QPushButton
from View.Page import Page
from myconfig import * 

class ChatListPage(Page):
    def __init__(self):
        super().__init__()
        self.setupUI()
    
    def setupUI(self):
        self.pageName.setText("CHAT ROOM")

        self.menuLine = QHBoxLayout()

        self.createRoomBtn = QPushButton()
        self.createRoomBtn.setIcon(QIcon(ADD_ICON))
        self.createRoomBtn.resize(QSize(26,26))


        self.roomSearchText = QLineEdit()

        self.roomSearchBtn = QPushButton()
        self.roomSearchBtn.resize(QSize(100, 30))
        self.roomSearchBtn.setIcon(QIcon(SEARCH_ICON))
        self.roomSearchBtn.resize(QSize(26, 26))
        self.roomSearchBtn.setIconSize(QSize(26, 26))

        self.roomSearchBtn.clicked.connect(self.clickRoomSearchBtn)

        # 여기에 chat list 를 QListWidget()사용해서 넣기 

        self.userSearchText = QLineEdit()

        self.userSearchBtn = QPushButton()
        self.userSearchBtn.resize(QSize(100, 30))
        self.userSearchBtn.setIcon(QIcon(SEARCH_ICON))
        self.userSearchBtn.setIconSize(QSize(26, 26))

        # 여기에 user list 를 QListWidget()사용해서 넣기 

        self.pageLayout.addWidget(self.pageName, 0, 2)
        self.pageLayout.addWidget(self.createRoomBtn, 1, 0)
        self.pageLayout.addWidget(self.roomSearchText, 1, 1)
        self.pageLayout.addWidget(self.roomSearchBtn, 1, 2)

        self.pageLayout.addWidget(self.userSearchText, 1, 3)
        self.pageLayout.addWidget(self.userSearchBtn, 1, 4)

        self.setLayout(self.pageLayout)
        
    def clickRoomSearchBtn(self):
        self.vc.instance().changePage(CHAT_ROOM)
        
    def clickUserSearchBtn(self):
        msg = AlertBox("user Search", "HI")
        msg.exec_()