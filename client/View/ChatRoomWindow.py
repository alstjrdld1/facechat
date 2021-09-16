from PyQt5.QtWidgets     import QApplication, QMainWindow
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

        # print("\n CHAT ROOM WINDOW CURRENT SIZE : ", self.size())

    def closeEvent(self, event):
        print("\n Close Event Called")
        
        print("\n face chat dock close ", self.faceChatDock.close())
        print("\n text chat dock close " , self.textChatDock.close())
        
        del(self.textChatDock)
        del(self.faceChatDock)

        event.accept()