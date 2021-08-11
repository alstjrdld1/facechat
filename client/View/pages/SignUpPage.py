from myconfig import *
from Control.Controller import Controller
from View.dialogs.AlertBox import AlertBox
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from View.pages.Page import Page

class SignUpPage(Page):
    def __init__(self):
        self.controller = Controller()
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.pageName.setText("SIGN UP PAGE")

        self.nameLabel = QLabel("NAME : ")
        self.name = QLineEdit()

        self.phoneLabel = QLabel("PHONE NUMBER : ")
        self.phone = QLineEdit()

        self.emailLabel = QLabel("EMAIL : ")
        self.email = QLineEdit()

        self.nickNameLabel = QLabel("NICK NAME : ")
        self.nickName = QLineEdit()

        self.idLabel = QLabel("ID : ")
        self.id = QLineEdit()

        self.passwordLabel = QLabel("PASSWORD : ")
        self.password = QLineEdit()

        self.greetingLabel = QLabel("Greeting : ")
        self.greeting = QLineEdit()

        self.signUpButton = QPushButton("SIGN UP")
        self.signUpButton.clicked.connect(self.clickSignUpBtn)
        
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
        self.pageLayout.addWidget(self.signUpButton, 8, 1)

        self.emptyLabel = QLabel()
        self.pageLayout.addWidget(self.emptyLabel, 1, 2)

        self.setLayout(self.pageLayout)
    
    def clickSignUpBtn(self):
        result = self.controller.instance().signUp(self.name.text(), self.phone.text(), self.email.text(), self.nickName.text(), self.id.text(), self.password.text(), self.greeting.text())
        
        # IF SIGN UP COMPLETE
        if result:
            msg = QMessageBox.question(self, "SIGN UP", "Do you want to add Face ID?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if(msg == QMessageBox.Yes):
                self.controller.instance().faceRegister()

            self.vc.instance().changePage(USER_ROOM)

        # ELSE SHOW ERROR MESSAGE
        else: 
            msg = AlertBox("SIGN UP ERROR", "ID OR PHONE NUMBER IS USING")
            msg.exec_()
            self.vc.instance().goBack()
    
        return None
 