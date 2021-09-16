from PyQt5.QtCore import *
from View.mydocks.Dock import Dock
from PyQt5.QtWidgets import *
import View.mydocks.TextChatClient as client

from myconfig import *

class TextChatDock(Dock):
    
    def __init__(self):
        
        super().__init__()
        self.c = client.ClientSocket(self)

        if(self.c.connectServer(SERVER_IP, int(PORT))):
            print("Chat Server Connected")
        else:
            print("Chat Server Connect Fail")

        self.setupUI()

    def __del__(self):
        self.c.stop()

    def setupUI(self):
        self.setWindowTitle("Text chat dock")
        self.setMinimumSize(QSize(300, 700))
        self.widgetContent = QWidget()

        widgetLayout = QVBoxLayout()
        sendChatLayout = QHBoxLayout()
        
        self.textMsg = QTextEdit()
        self.textMsg.setFixedHeight(50)

        self.sendBtn = QPushButton("SEND")
        self.sendBtn.clicked.connect(self.sendMsg)
        self.sendBtn.setFixedHeight(50)

        sendChatLayout.addWidget(self.textMsg)
        sendChatLayout.addWidget(self.sendBtn)

        self.recvmsg = QListWidget()

        widgetLayout.addWidget(self.recvmsg)
        widgetLayout.addLayout(sendChatLayout)

        self.widgetContent.setLayout(widgetLayout)
        self.setWidget(self.widgetContent)

        print("\n TEXT CHAT DOCK SIZE : ", self.size())
 
    def updateMsg(self, msg):
        self.recvmsg.addItem(QListWidgetItem(msg))

    def updateDisconnect(self):
        pass 
        # self.btn.setText('접속')
 
    def sendMsg(self):
        sendmsg = self.textMsg.toPlainText()    

        item = QListWidgetItem()
        item.setText(sendmsg)
        item.setTextAlignment(Qt.AlignRight)
        self.recvmsg.addItem(item)

        self.c.send(sendmsg)        
        self.textMsg.clear()
 
    def clearMsg(self):
        self.recvmsg.clear()
 
    def closeEvent(self, e):
        self.c.stop()