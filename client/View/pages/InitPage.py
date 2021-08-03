from View.dialogs.AlertBox import *

class InitPage(QWidget):
    
    def __init__(self):
        
        from Control.ViewController import ViewController
        from Control.Controller import Controller

        self.vc = ViewController()
        self.controller = Controller()

        super().__init__()
        self.initUI()

    def initUI(self):
        ###### Contents Layout 
        self.buttonLayout = QVBoxLayout() 

        ###### Page labels
        self.label = QLabel(PROGRAM_NAME, self)
        self.label.setStyleSheet(FONT_SIZE_LARGE)
        
        # self.label.move(200, 600)
        self.label.resize(200, 20)
        self.label.setAlignment(Qt.AlignCenter)

        ###### Buttons
        self.loginBtn = QPushButton('LOGIN')
        self.loginBtn.clicked.connect(self.loginButtonClicked)

        self.signUpBtn = QPushButton('SIGN UP')
        self.signUpBtn.clicked.connect(self.signUpButtonClicked)

        self.findIDBtn = QPushButton('FIND ID')
        self.findIDBtn.clicked.connect(self.finfIDButtonClicked)

        self.findPWBtn = QPushButton('FIND PW')
        self.findPWBtn.clicked.connect(self.findPWButtonClicked)

        # self.buttonLayout.addWidget(self.topWidget)
        self.buttonLayout.addWidget(self.label)
        self.buttonLayout.addWidget(self.loginBtn)
        self.buttonLayout.addWidget(self.signUpBtn)
        self.buttonLayout.addWidget(self.findIDBtn)
        self.buttonLayout.addWidget(self.findPWBtn)

        self.setLayout(self.buttonLayout)
        
    def loginButtonClicked(self):
        loginSuccess = self.controller.instance().faceLogin()
    
        if(loginSuccess):
            self.vc.instance().changePage(USER_ROOM)
        else:
            self.vc.instance().changePage(LOGIN)

    def signUpButtonClicked(self):
        self.vc.instance().changePage(SIGN_UP)
    
    def finfIDButtonClicked(self):
        self.vc.instance().changePage(FIND_ID)

    def findPWButtonClicked(self):
        self.vc.instance().changePage(FIND_PW)

    def backButton(self):
        reply = QMessageBox.question(self, 'Message', 'Backbutton Clicked',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
