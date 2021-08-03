from View.dialogs.AlertBox import AlertBox
from View.mydocks.Dock import Dock
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QListWidget, QListWidgetItem, QPushButton, QTextEdit, QVBoxLayout, QWidget
import View.mydocks.client as client

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

        self.widgetContent = QWidget()

        widgetLayout = QVBoxLayout()
        sendChatLayout = QHBoxLayout()
        
        self.textMsg = QTextEdit()
        self.textMsg.setFixedHeight(50)

        self.sendBtn = QPushButton("SEND")
        self.sendBtn.clicked.connect(self.sendMsg)

        sendChatLayout.addWidget(self.textMsg)
        sendChatLayout.addWidget(self.sendBtn)

        self.recvmsg = QListWidget()

        widgetLayout.addWidget(self.recvmsg)
        widgetLayout.addLayout(sendChatLayout)

        self.widgetContent.setLayout(widgetLayout)
        self.setWidget(self.widgetContent)
 
    def updateMsg(self, msg):
        self.recvmsg.addItem(QListWidgetItem(msg))
 
    def updateDisconnect(self):
        pass 
        # self.btn.setText('접속')
 
    def sendMsg(self):
        sendmsg = self.textMsg.toPlainText()       
        self.c.send(sendmsg)        
        self.textMsg.clear()
 
    def clearMsg(self):
        self.recvmsg.clear()
 
    def closeEvent(self, e):
        self.c.stop()