import pickle
import time
from myconfig import *
from View.mydocks.faceClient import FaceClientSocket
from threading import *

import cv2
import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from View.mydocks.Dock import Dock

class SendVideoThread(QThread):

    change_pixmap_signal = pyqtSignal(np.ndarray)
    
    def __init__(self):
        super().__init__()
        self._run_flag = True

    def __del__(self):
        self.stop()

    def run(self):

        cap = cv2.VideoCapture(0)
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret : 
                blurred = self.faceBlur(cv_img)
                self.change_pixmap_signal.emit(blurred)

        cap.release()
    
    def stop(self):
        print("\n VIDEO thread stop method called")
        self._run_flag = False
        self.wait()

    def faceBlur(self , img):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv,  (0, 75, 40), (180, 255, 255))

        mask_3d = np.repeat(mask[:, :, np.newaxis], 3, axis =2)
        blurred_frame = cv2.GaussianBlur(img, (25, 25), 0)
        frame = np.where(mask_3d == (255, 255, 255), img, blurred_frame)

        return frame

count = 0

class FaceChatDock(Dock):
    display_width = 0
    display_height = 0
    frameList = []
    current_user_number = 0
    
    def __init__(self):
        from Control.Controller import Controller
        
        self.controller = Controller()
        
        self.c = FaceClientSocket(self)

        if(self.c.connectServer(SERVER_IP, int(FACE_CHAT_PORT))):
            print("FACE CHAT SERVER CONNECTED")
        else:
            print("FACE CHAT SERVER CONNECT FAIL")
                        
        super().__init__()
        self.setupUI()

    def __del__(self):
        del(self.c)

        self.stop()

    def stop(self):
        self.bConnect = False       
        if hasattr(self, 'client'):  
            self.c.close()
            del(self.c)
            print('Client Stop') 

    def setupUI(self):

        self.myNick = self.controller.instance().getCurrentUser().getNickName()
 
        self.setWindowTitle("Face chat dock")

        self.h1box = QHBoxLayout()
        self.h2box = QHBoxLayout()
        self.h3box = QHBoxLayout()
        self.h4box = QHBoxLayout()
        self.updateVideoUI()

        vbox = QVBoxLayout()
        vbox.addLayout(self.h1box)
        vbox.addLayout(self.h2box)
        vbox.addLayout(self.h3box)
        vbox.addLayout(self.h4box)

        widget = QWidget()
        widget.setLayout(vbox)

        self.setWidget(widget)

        ### About Thread 
        self.thread = SendVideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()

        self.c.recv.recv_signal.connect(self.update_other_image)
        
        # print("CURRENT VIDEO CHAT DOCK HEIGHT :", self.height())
        # print("CURRENT VIDEO CHAT DOCK WIDTH :", self.width())

        # print("VIDEO CHAT DOCK SIZE :", self.size())
        # print("VIDEO CHAT DOCK SIZE :", self.frameSize())


    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    def caculateDisplaySize(self, number):
        if(number == 1):
            self.display_width = self.width()
            self.display_height = self.height()
        elif(number <= 4):
            self.display_width = int(self.width() / number)
            self.display_height = int(self.height() / number)
        else:
            self.display_width = int(self.width() / 4)
            self.display_height = int(self.height() / 4)

    def updateVideoUI(self):
        # self.member_num = self.controller.instance().getChatRoomUserNumber() # real version 
        self.member_num = 12 # test version 
        self.caculateDisplaySize(self.member_num)
        
        for count in range(self.member_num):
            createFrame = QLabel()
            createFrame.resize(self.display_width, self.display_height)
            # print("{} frame width : {}, height : {}".format(count, self.display_width, self.display_height))
            createFrame.setStyleSheet("border: 1px solid black;")

            if(int(count/4) == 0):
                self.h1box.addWidget(createFrame)
            elif(int(count/4) == 1):
                self.h2box.addWidget(createFrame)
            elif(int(count/4) == 2):
                self.h3box.addWidget(createFrame)
            elif(int(count/4) == 3):
                self.h4box.addWidget(createFrame)

            self.frameList.append(createFrame)
            # print("{} Frame added".format(count))
        
    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):

        cv2.putText(cv_img,self.myNick,(260,450), cv2.FONT_HERSHEY_COMPLEX,1,(250,120,255),2)

        qt_img = self.convert_cv_qt(cv_img)
        # self.my_image_label.setPixmap(qt_img) 
        # self.frameList[0].setPixmap(qt_img) 

        # print(cv_img.shape)
        # self.c.send(cv_img) 
        sendingThread = Thread(target=self.c.send, args=(cv_img, ))
        sendingThread.start() 
        sendingThread.join()

    @pyqtSlot(np.ndarray)
    def update_other_image(self, cv_img):
        qt_img = self.convert_cv_qt(cv_img)
        users = self.controller.instance().getChatRoomUserNumber()

        if self.current_user_number != users:
            self.current_user_number = users
            self.caculateDisplaySize(self.current_user_number)

        # print("users : ", users)
        global count
        
        self.frameList[int(count%users)].setPixmap(qt_img)

        count += 1
        if count >= 999 :
            count = 0
        # for fl in self.frameList:
        #     count += 1
        #     # print("FOR LOOP : ", count)
        #     if count == 1 :
        #         continue
        #     fl.setPixmap(qt_img)
        #     # print("SET PIXMAP CLEAR")
            
        # self.frameList[1].setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format  = QImage(rgb_image.data, w, h , bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.display_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
