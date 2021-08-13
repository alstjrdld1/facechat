from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import *

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

class ChatRoom(QMainWindow):
    def __init__(self, parent=None):
        from View.mydocks.FaceChatDock import FaceChatDock
        from View.mydocks.TextChatDock import TextChatDock
        super(ChatRoom, self).__init__(parent)
        self.textChatDock = TextChatDock()
        self.faceChatDock = FaceChatDock()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Face Chat")
        self.setMinimumSize(1200, 700)

        self.addDockWidget(Qt.LeftDockWidgetArea, self.faceChatDock)
        self.addDockWidget(Qt.RightDockWidgetArea, self.textChatDock)

    def closeEvent(self, event):
        self.faceChatDock.close()
        self.textChatDock.close()