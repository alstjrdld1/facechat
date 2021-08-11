from View.dialogs.AlertBox import AlertBox
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import *
from win32api import GetSystemMetrics

from View.dialogs.CustomDialog import * 
from Control.SingleTon import * 

class LoginPage(QWidget):
    def __init__(self):
        from Control.ViewController import ViewController
        self.vc = ViewController()
        super().__init__()
        self.setupUI()
        
    def setupUI(self):
        self.myLayout = QVBoxLayout()

        self.loginBtn = QPushButton()
        self.loginBtn.setText('LOGIN')
        self.loginBtn.clicked.connect(self.loginButtonClick)

        self.backBtn = QPushButton()
        self.backBtn.setText("GO BACK")
        self.backBtn.clicked.connect(self.backBtnClick)
        
        self.myLayout.addWidget(self.loginBtn)
        self.myLayout.addWidget(self.backBtn)
        self.setLayout(self.myLayout)
    
    def loginButtonClick(self):
        msg = LoginDialog()
        msg.exec_() 

    def backBtnClick(self):
        self.vc.instance().goBack()


class LoginDialog(CustomDialog):
    loginState = False

    def __init__(self):
        from Control.Controller import Controller
        from Control.ViewController import ViewController
        self.controller = Controller()
        self.vc = ViewController()

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
        self.loginState = self.controller.instance().textLogin(self.lineEdit1.text(), self.lineEdit2.text())
        if(self.loginState):
            self.vc.instance().changePage(USER_ROOM)
            self.close()
        else:
            msg = AlertBox("LOGIN ERROR", "ID OR PASSWORD IS WRONG")
            msg.exec_()

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