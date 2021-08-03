from PyQt5.QtWidgets import QApplication
from View.MainWindow import MainWindow
from Control.ViewController import ViewController
from View.pages.InitPage import * 

import sys 

if __name__ == '__main__':    
    app =QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.show()

    ViewController().instance().registerMainWindow(mainWindow)

    sys.exit(app.exec_())