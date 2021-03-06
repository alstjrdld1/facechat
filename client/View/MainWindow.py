from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from myconfig import * 

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()
    
    def setupUI(self):
        # Window Title and Icon 
        self.setWindowTitle(PROGRAM_NAME) # Window name 
        self.setWindowIcon(QIcon(WINDOW_ICON))
        
        # Window Size and Initial location 
        # self.move(660, 290) # Initialize the window location when program start
        self.setFixedSize(WINDOW_SIZE) # Inital size of the window when program start 
        self.setStyleSheet(BACKGROUND_COLOR)
    
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        return super().closeEvent(a0)
        