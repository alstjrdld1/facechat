from View.mydocks.Dock import Dock
from PyQt5.QtWidgets import QLabel

class FaceChatDock(Dock):
    def __init__(self):
        super().__init__()
        self.setupUI()


    def setupUI(self):
        self.btn = QLabel("FACE CHAT DOCK")
