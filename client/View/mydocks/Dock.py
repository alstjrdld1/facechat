import socket
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QDockWidget 

class Dock(QDockWidget):

    def __init__(self):
        super().__init__()
        