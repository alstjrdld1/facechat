from PyQt5.QtCore import *
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import *

from myconfig import *

class CustomDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setGeometry(1100, 200, 300, 200)
        self.setWindowIcon(QIcon(WINDOW_ICON))
        self.setStyleSheet(BACKGROUND_COLOR)



