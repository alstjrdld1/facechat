import socket
from threading import *

import cv2
import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from View.mydocks.Dock import Dock


class SendVideoThread(QThread):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):

        cap = cv2.VideoCapture(0)
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret : 
                blurred = self.faceBlur(cv_img)
                video = blurred.flatten().tostring()

                self.change_pixmap_signal.emit(blurred)
        
        cap.release()
    
    def stop(self):
        self._run_flag = False
        self.wait()

    def faceBlur(self , img):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv,  (0, 75, 40), (180, 255, 255))

        mask_3d = np.repeat(mask[:, :, np.newaxis], 3, axis =2)
        blurred_frame = cv2.GaussianBlur(img, (25, 25), 0)
        frame = np.where(mask_3d == (255, 255, 255), img, blurred_frame)

        return frame
    

class ReceiveVideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        
        cap = cv2.VideoCapture(0)
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret : 
                self.change_pixmap_signal.emit(cv_img)
        
        cap.release()
    
    def stop(self):
        self._run_flag = False
        self.wait()

class FaceChatDock(Dock):
    otherUser = False
    def __init__(self):
        from Control.Controller import Controller
        self.controller = Controller
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Face chat dock")

        self.display_width = 450  
        self.display_height = 336

        self.my_image_label = QLabel()
        self.my_image_label.resize(self.display_width, self.display_height)

        self.other_image_label = QLabel()
        self.other_image_label.resize(self.display_width, self.display_height)

        h1box = QHBoxLayout()
        h1box.addWidget(self.my_image_label)
        h1box.addWidget(self.other_image_label)

        h2box = QHBoxLayout()
        name1 = QLabel(self.controller.instance().getCurrentUser().getNickName())
        name2 = QLabel()
        
        if self.otherUser:
            name2.setText("other user")
            
        else :
            name2.setText("NONE")
        name1.setAlignment(Qt.AlignCenter)
        name2.setAlignment(Qt.AlignCenter)

        h2box.addWidget(name1)
        h2box.addWidget(name2)

        vbox = QVBoxLayout()
        vbox.addLayout(h1box, 2)
        vbox.addLayout(h2box)

        widget = QWidget()
        widget.setLayout(vbox)

        self.setWidget(widget)

        ### About Thread 
        self.thread1 = SendVideoThread()
        self.moveToThread(self.thread1)
        self.thread1.change_pixmap_signal.connect(self.update_image)
        self.thread1.start()

        # self.thread2 = ReceiveVideoThread()
        # self.moveToThread(self.thread2)
        # self.thread2.change_pixmap_signal.connect(self.update_other_image)
        # self.thread2.start()
        

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()
    
    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        qt_img = self.convert_cv_qt(cv_img)
        self.my_image_label.setPixmap(qt_img)

    @pyqtSlot(np.ndarray)
    def update_other_image(self, cv_img):
        qt_img = self.convert_cv_qt(cv_img)
        self.other_image_label.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format  = QImage(rgb_image.data, w, h , bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.display_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
