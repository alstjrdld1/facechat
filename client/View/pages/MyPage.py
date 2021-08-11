from View.dialogs.AlertBox import AlertBox
from PyQt5.QtWidgets import QLineEdit, QPushButton
from View.pages.Page import *

class MyPage(Page):
    def __init__(self):
        from Control.Controller import Controller 
        self.controller = Controller()
        super().__init__()
        self.setupUI()

    def setupUI(self):
        me = self.controller.instance().getCurrentUser()
        self.pageName.setText("MY PAGE")
        self.pageLayout.addWidget(self.pageName, 0, 1)

        self.nameLabel = QLabel("NAME : ")
        self.name = QLineEdit()
        self.name.setText(me.getName())

        self.phoneLabel = QLabel("PHONE NUMBER : ")
        self.phone = QLabel()
        self.phone.setText(me.getPhNum())

        self.emailLabel = QLabel("EMAIL : ")
        self.email = QLineEdit()
        self.email.setText(me.getEmail())


        self.nickNameLabel = QLabel("NICK NAME : ")
        self.nickName = QLineEdit()
        self.nickName.setText(me.getNickName())

        self.idLabel = QLabel("ID : ")
        self.id = QLabel()
        self.id.setText(me.getId())

        self.passwordLabel = QLabel("PASSWORD : ")
        self.password = QLineEdit()
        self.password.setText(me.getPw())

        
        self.greetingLabel = QLabel("GREETING : ")
        self.greeting = QLineEdit()
        self.greeting.setText(me.getGreeting())

        self.changeInfoButton = QPushButton("CHANGE")
        self.changeInfoButton.clicked.connect(self.clickChangeInfobtn)

        self.backButton = QPushButton("BACK")
        self.backButton.clicked.connect(self.backBtn)
        
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
        self.pageLayout.addWidget(self.greetingLabel, 7, 0)
        self.pageLayout.addWidget(self.greeting, 7, 1)
        self.pageLayout.addWidget(self.backButton, 8, 0)
        self.pageLayout.addWidget(self.changeInfoButton, 8, 1)

        self.setLayout(self.pageLayout)

    
    def clickChangeInfobtn(self):   
        self.controller.instance().changeUserInfo(self.name.text(), self.phone.text(), self.email.text(), self.nickName.text(), self.id.text(), self.password.text(), self.greeting.text())
    
    def backBtn(self):
        self.vc.instance().goBack()
