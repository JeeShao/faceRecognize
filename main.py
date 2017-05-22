#!/usr/bin/env python
#  -- coding:utf-8 --
# #@Time  : 2017/3/22
# #@Author: Jee
import sys
import cv2
from PyQt4 import QtGui
from PyQt4.QtGui import *
from ui import mainwindow
from camera import Video
from configure import config
from PyQt4.QtGui import QApplication
# from PyQt4.QtGui import QPalette, QPixmap, QBrush

def main():
    model = cv2.face.createLBPHFaceRecognizer(threshold=70)
    model.load(config.TRAINING_FILE)
    
    video = Video.Video(1)
    video.release()
    video.setFrameSize(640, 480)
    video.setFPS(30)

    QtApp = QApplication(sys.argv)
    
    mainWindow = mainwindow.Ui_MainWindow()
    mainWindow.setModel(model)
    # mainWindow.center()

    mainWindow.setWindowTitle("FRS")
    # mainWindow.setStyleSheet("mainWindow{background-image: url(:E:/OneDrive/faceRecognize/1.jpg)}")
    # mainWindow.setAutoFillBackground(True)
    # palette = QPalette()
    # pixmap = QPixmap("1.jpg")
    # palette.setBrush(QPalette.Background, QBrush(pixmap))
    # mainWindow.setPalette(palette)
    # mainWindow.setAutoFillBackground(True)


    # icon = QtGui.QIcon()
    # icon.addPixmap(QtGui.QPixmap('E:/OneDrive/faceRecognize/ui/css/qq.ico'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    # mainWindow.setWindowIcon(icon)

    mainWindow.show()
    mainWindow.setVideo(video)
    mainWindow.raise_()
    
    QtApp.exec_()

if __name__ == '__main__':
    main()
