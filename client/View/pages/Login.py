from PyQt5.QtWidgets import * 
from PyQt5.QtGui import *
from win32api import GetSystemMetrics

from View.dialogs.CustomDialog import * 
from Control.SingleTon import * 

class LoginPage(QWidget):
    def __init__(self):
        super().__init__()

        self.myLayout = QVBoxLayout()

        self.loginBtn = QPushButton()
        self.loginBtn.setText('LOGIN')
        
        self.myLayout.addWidget(self.loginBtn)
        self.setLayout(self.myLayout)

class LoginDialog(CustomDialog):
    def __init__(self):
        super().__init__()
        self.setupUI()

        self.id = None
        self.password = None

    def setupUI(self):
        self.setWindowTitle("Sign In")
        
        label1 = QLabel("ID : ")
        label2 = QLabel("Password : ")

        self.lineEdit1 = QLineEdit()
        self.lineEdit2 = QLineEdit()
        self.pushButton1 = QPushButton("SIGN IN")
        self.pushButton1.clicked.connect(self.pushButtonClicked)
        
        layout = QGridLayout()
        layout.addWidget(label1, 0, 0)
        layout.addWidget(self.lineEdit1, 0, 1)
        layout.addWidget(self.pushButton1, 1, 2)
        layout.addWidget(label2, 1, 0)
        layout.addWidget(self.lineEdit2, 1, 1)

        self.setLayout(layout)

    def pushButtonClicked(self):
        self.id = self.lineEdit1.text()
        self.password = self.lineEdit2.text()
        self.close()

class FaceLoginDialog(CustomDialog):
    loginState = True 

    def __init__(self):
        super().__init__()
        self.resize()
    
    def resize(self):
        ### Call camera 

        self.camHeight = 480
        self.camWidth = 720

        monitorWidth = GetSystemMetrics(0)
        monitorHeight = GetSystemMetrics(1)
    
        windowLoc = QRect(monitorWidth/2 - self.camWidth/2, monitorHeight/2 - self.camHeight/2, self.camWidth, self.camHeight)

        self.setGeometry(windowLoc)
        
    def getLoginState(self):
        return self.loginState