import sys 
from PyQt5.QtWidgets import * 
from Models import *

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Hello world')
        self.move(300, 300)
        self.resize(400, 200)
        self.show()

if __name__ == '__main__':
    app =QApplication(sys.argv)
    
    minseok = USERS()
    room1 = ROOM(1)

    print(room1.number)
    ex = MyApp()
    sys.exit(app.exec_())

