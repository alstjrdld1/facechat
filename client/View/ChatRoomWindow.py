from PyQt5.QtWidgets     import QApplication, QMainWindow
from PyQt5.QtCore import *
from View.mydocks.AudioClient import *
from threading import * 
from myconfig import *
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True) # 고화질 모니터에서도 가능하게 함 enable on high resolution monitor

class ChatRoom(QMainWindow):
    def __init__(self, parent=None):
        from View.mydocks.FaceChatDock import FaceChatDock
        from View.mydocks.TextChatDock import TextChatDock
        super(ChatRoom, self).__init__(parent)
        self.textChatDock = TextChatDock()
        self.faceChatDock = FaceChatDock()

        
        # self.thread = AudioClient(SERVER_IP, AUDIO_CHAT_PORT)
        # self.thread.start()

        self.audio = AudioClient(SERVER_IP, AUDIO_CHAT_PORT)

        self.setupUI()
    
    def __del__(self):
        # del(self.audio)
        
        # self.audio.stop()
        # del(self.audio)
        pass

    def setupUI(self):
        self.setWindowTitle("Face Chat")
        self.setMinimumSize(1200, 700)

        self.addDockWidget(Qt.LeftDockWidgetArea, self.faceChatDock)
        self.addDockWidget(Qt.RightDockWidgetArea, self.textChatDock)
        
        self.audio_thread = Thread(target = self.audio.start, args=())
        self.audio_thread.start()

        # print("\n CHAT ROOM WINDOW CURRENT SIZE : ", self.size())

    def closeEvent(self, event):
        print("\n Close Event Called")
        
        print("\n face chat dock close ", self.faceChatDock.close())
        print("\n text chat dock close " , self.textChatDock.close())
        
        # self.c.stop()
        del(self.audio)
        # del(self.c)
        del(self.audio_thread)

        # del(self.textChatDock)
        # del(self.faceChatDock)

        event.accept()