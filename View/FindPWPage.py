from View.AlertBox import AlertBox
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton
from View.Page import Page


class FindPWPage(Page):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.pageName.setText("FIND PW PAGE")

        self.nameLabel = QLabel("NAME : ")
        self.name = QLineEdit()

        self.phoneLabel = QLabel("PHONE NUMBER : ")
        self.phone = QLineEdit()

        self.idLabel = QLabel("ID : ")
        self.id = QLineEdit()

        self.findPWButton = QPushButton("FIND PW")
        self.findPWButton.clicked.connect(self.findPW)

        ### ADD WIDGET
        self.pageLayout.addWidget(self.pageName, 0, 1)
        self.pageLayout.addWidget(self.nameLabel, 1, 0)
        self.pageLayout.addWidget(self.name, 1, 1)

        self.pageLayout.addWidget(self.phoneLabel, 2, 0)
        self.pageLayout.addWidget(self.phone, 2, 1)

        self.pageLayout.addWidget(self.idLabel, 3, 0)
        self.pageLayout.addWidget(self.id, 3, 1)

        self.pageLayout.addWidget(self.findPWButton, 4, 1)

        self.setLayout(self.pageLayout)

    def findPW(self):
        
        # send Informations to server with controller 
        
        if(True):
            msg = AlertBox("FIND PW", "YOUR PASSWORD IS \n " + "minstone")
            msg.exec_()
        else:
            msg = AlertBox("FIND ID", "SOME PROBLEM IN HERE")

        self.vc.instance().goBack()