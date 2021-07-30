from View.FindPWPage import FindPWPage
from View.FindIDPage import FindIDPage
from PyQt5.QtWidgets import QApplication
from View.InitPage import InitPage
from Control.SingleTon import * 


class Controller(SingletonInstane):
    
    count = 0
    def __init__(self):
        super().__init__()

    def countPlus(self):
        self.count += 1
    
    def getCount(self):
        return self.count
    
    