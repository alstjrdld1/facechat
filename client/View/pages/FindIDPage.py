
from Control.Controller import Controller
from View.dialogs.AlertBox import AlertBox
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton
from View.pages.Page import Page


class FindIDPage(Page):
    def __init__(self):
        self.controller = Controller()
        super().__init__()
        self.setupUI()
    
    def setupUI(self):
        self.pageName.setText("FIND ID PAGE")

        self.nameLabel = QLabel("NAME : ")
        self.name = QLineEdit()

        self.phoneLabel = QLabel("PHONE NUMBER : ")
        self.phone = QLineEdit()

        self.findIDButton = QPushButton("FIND ID")
        self.findIDButton.clicked.connect(self.findID)

        self.pageLayout.addWidget(self.pageName, 0, 1)
        self.pageLayout.addWidget(self.nameLabel, 1, 0)
        self.pageLayout.addWidget(self.name, 1, 1)

        self.pageLayout.addWidget(self.phoneLabel, 2, 0)
        self.pageLayout.addWidget(self.phone, 2, 1)

        self.pageLayout.addWidget(self.findIDButton, 3, 1)

        self.setLayout(self.pageLayout)


    def findID(self):
        
        # send Informations to server with controller 
        id = self.controller.instance().getId(self.phone.text(), self.name.text())

        if(id):
            msg = AlertBox("FIND ID", "YOUR ID IS \n " + id)
            msg.exec_()
        else:
            msg = AlertBox("FIND ID", "SOME PROBLEM IN HERE")
            msg.exec_()
        
        self.vc.instance().goBack()