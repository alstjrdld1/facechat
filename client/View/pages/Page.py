from PyQt5.QtCore import center
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QGridLayout, QLabel, QWidget
from PyQt5.QtCore import *

from myconfig import *

class Page(QWidget):
    
    pageName = ""
    pageLayout = ""

    def __init__(self):
        super().__init__()

        self.pageName = QLabel()
        self.pageLayout = QGridLayout()
        
        self.pageLayout.addWidget(self.pageName)
        self.pageName.setAlignment(Qt.AlignCenter)
        
        self.setupUI()
        from Control.ViewController import ViewController
        self.vc = ViewController()

    def setupUI(self):
        self.resize(WIDGET_SIZE)
        self.setStyleSheet(BACKGROUND_COLOR)
        self.setLayout(self.pageLayout)