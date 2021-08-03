from View.dialogs.AlertBox import AlertBox
from PyQt5.QtWidgets import QLineEdit, QPushButton
from View.pages.Page import *

class MyPage(Page):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.pageName.setText("MY PAGE")
        self.pageLayout.addWidget(self.pageName, 0, 1)

        self.nameLabel = QLabel("NAME : ")
        self.name = QLineEdit()
        self.name.setPlaceholderText("MINSTONE")

        self.phoneLabel = QLabel("PHONE NUMBER : ")
        self.phone = QLineEdit()
        self.phone.setPlaceholderText("010-1111-1111")

        self.emailLabel = QLabel("EMAIL : ")
        self.email = QLineEdit()
        self.email.setPlaceholderText("Aab@naver.com")


        self.nickNameLabel = QLabel("NICK NAME : ")
        self.nickName = QLineEdit()
        self.nickName.setPlaceholderText("MINSTONE")

        self.idLabel = QLabel("ID : ")
        self.id = QLineEdit()
        self.id.setPlaceholderText("KMS1998")

        self.passwordLabel = QLabel("PASSWORD : ")
        self.password = QLineEdit()
        self.password.setPlaceholderText("1111111")

        self.changeInfoButton = QPushButton("CHANGE")
        self.changeInfoButton.clicked.connect(self.clickChangeInfobtn)
        
        self.pageLayout.addWidget(self.pageName, 0, 1)
        self.pageLayout.addWidget(self.nameLabel, 1, 0)
        self.pageLayout.addWidget(self.name, 1, 1)
        self.pageLayout.addWidget(self.phoneLabel, 2, 0)
        self.pageLayout.addWidget(self.phone, 2, 1)
        self.pageLayout.addWidget(self.emailLabel, 3, 0)
        self.pageLayout.addWidget(self.email, 3, 1)
        self.pageLayout.addWidget(self.nickNameLabel, 4, 0)
        self.pageLayout.addWidget(self.nickName, 4, 1)
        self.pageLayout.addWidget(self.idLabel, 5, 0)
        self.pageLayout.addWidget(self.id, 5, 1)
        self.pageLayout.addWidget(self.passwordLabel, 6, 0)
        self.pageLayout.addWidget(self.password, 6, 1)
        self.pageLayout.addWidget(self.changeInfoButton, 7, 1)

        self.setLayout(self.pageLayout)

    
    def clickChangeInfobtn(self):
        # Send Changed Information to server 

        # IF SUCCESS ALERT SUCCESS MESSAGE 
        msg = AlertBox("CHAGNE INFO", "CHANGED!")
        msg.exec_()

        # ELSE SHOW FAILURE ALERT 

        # GO TO USER ROOM
        self.vc.instance().goBack()