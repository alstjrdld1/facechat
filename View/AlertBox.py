from PyQt5.QtGui import *
from PyQt5.QtCore import * 
from PyQt5.QtWidgets import * 

from myconfig import *

class AlertBox(QDialog):

    def __init__(self, title, message):
        super().__init__()

        self.windowTitle = title
        self.alertMessage = message
        self.setStyleSheet(BACKGROUND_COLOR)

        self.setupUI()

    def setupUI(self):
        self.setGeometry(810, 440, 300, 200)
        self.setWindowTitle(self.windowTitle)
        self.setWindowIcon(QIcon(WINDOW_ICON))

        message = QLabel(self.alertMessage)
        message.setAlignment(Qt.AlignCenter)

        self.closeButton = QPushButton("OK")
        self.closeButton.clicked.connect(self.pushButtonClicked)

        layout = QGridLayout()
        layout.addWidget(message, 1, 1)
        layout.addWidget(self.closeButton, 2, 1)

        self.setLayout(layout)

    def pushButtonClicked(self):
        self.close()




