from PyQt5 import QtCore
import cv2 

from View.mydocks.Dock import Dock
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class ShowVideo(QObject):

    flag = 0

    camera = cv2.VideoCapture(0)

    ret, image = camera.read()
    height, width = image.shape[:2]

    VideoSignal1 = pyqtSignal(QImage)
    VideoSignal2 = pyqtSignal(QImage)

    def __init__(self, parent=None):
        super(ShowVideo, self).__init__(parent)

    @pyqtSlot()
    def startVideo(self):
        global image

        run_video = True
        while run_video:
            ret, image = self.camera.read()
            color_swapped_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            qt_image1 = QImage(color_swapped_image.data,
                                    self.width,
                                    self.height,
                                    color_swapped_image.strides[0],
                                    QImage.Format_RGB888)
            self.VideoSignal1.emit(qt_image1)


            if self.flag:
                img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                img_canny = cv2.Canny(img_gray, 50, 100)

                qt_image2 = QImage(img_canny.data,
                                         self.width,
                                         self.height,
                                         img_canny.strides[0],
                                         QImage.Format_Grayscale8)

                self.VideoSignal2.emit(qt_image2)


            loop = QEventLoop()
            QTimer.singleShot(25, loop.quit) #25 ms
            loop.exec_()

    @pyqtSlot()
    def canny(self):
        self.flag = 1 - self.flag


class ImageViewer(QWidget):
    def __init__(self, parent=None):
        super(ImageViewer, self).__init__(parent)
        self.image = QImage()
        self.setAttribute(Qt.WA_OpaquePaintEvent)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(0, 0, self.image)
        self.image = QImage()

    def initUI(self):
        self.setWindowTitle('Test')

    @pyqtSlot(QImage)
    def setImage(self, image):
        if image.isNull():
            print("Viewer Dropped frame!")

        self.image = image
        if image.size() != self.size():
            self.setFixedSize(image.size())
        self.update()

class FaceChatDock(Dock):
    def __init__(self):
        super().__init__()
        self.setupUI()


    def setupUI(self):
        self.setWindowTitle("Face chat dock")

        self.camLayout = QHBoxLayout()

        thread = QtCore.QThread()
        thread.start()

        vid = ShowVideo()
        vid.moveToThread(thread)
        
        image_viewer1 = ImageViewer()
        image_viewer2 = ImageViewer()

        vid.VideoSignal1.connect(image_viewer1.setImage)
        vid.VideoSignal2.connect(image_viewer2.setImage)

        self.camLayout.addWidget(image_viewer1)
        self.camLayout.addWidget(image_viewer2)

        vid.startVideo()

        self.setLayout(self.camLayout)
        


