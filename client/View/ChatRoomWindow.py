from PyQt5 import QtGui
from View.mydocks.FaceChatDock import FaceChatDock
from View.mydocks.TextChatDock import TextChatDock

from PyQt5.QtWidgets import QDialog, QMainWindow
from PyQt5.QtCore import *

class ChatRoom(QMainWindow):
    def __init__(self, parent=None):
        super(ChatRoom, self).__init__(parent)
        self.textChatDock = TextChatDock()
        self.faceChatDock = FaceChatDock()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Face Chat")
        self.setGeometry(QRect(360, 190, 1200, 700))

        self.addDockWidget(Qt.LeftDockWidgetArea, self.faceChatDock)
        self.addDockWidget(Qt.RightDockWidgetArea, self.textChatDock)

    def closeEvent(self, event):
        self.faceChatDock.close()
        self.textChatDock.close()