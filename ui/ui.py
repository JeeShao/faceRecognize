#!/usr/bin/env python
#  -- coding:utf-8 --
# #@Time  : 2017/3/22
# #@Author: Jee
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from facerec import recognize, train
from facerec import face
from camera import VideoStream
from configure import config, userManager
from .soft_keyboard import *
import os
import cv2
import re
import shutil

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

#Qt css样式文件
# style = open('./ui/css/style.css').read()

#显示视频的Qt控件
#setRect当前一帧图像上画出方框，用于标记人脸的位置
#setRectColor设置方框的颜色
#setUserLabel在方框旁边添加识别信息，比如识别到的用户名
class VideoFrame(QtGui.QLabel):
        
    userName = None
    pen_faceRect = QtGui.QPen()
    pen_faceRect.setWidth(3) #设置画笔粗细3px
    pen_faceRect.setColor(QtGui.QColor(255, 0, 0))
    x = 0;y = 0;w = 0;h = 0
    
    def __init__(self, parent):
        QtGui.QLabel.__init__(self, parent)
        
    def setRect(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h
    
    def setRectColor(self, r, g, b):
        self.pen_faceRect.setColor(QtGui.QColor(r, g, b))

    def setUserLabel(self, userName):
        self.userName = userName

    def paintEvent(self, event):
        QtGui.QLabel.paintEvent(self,event)
        painter = QtGui.QPainter(self)
        painter.setPen(self.pen_faceRect)
        painter.drawRect(self.x, self.y, self.w, self.h)
        if self.userName is not None:
            painter.drawText(self.x, self.y+15, self.userName)

# 人脸录入界面
class FaceRegister(QWidget):
    faceRect = None
    captureFlag = 0
    personName = None
    recOver = False
    model = None

    def __init__(self, mainWindow):
        super(FaceRegister, self).__init__()

        self.mainWindow = mainWindow
        self.manager = userManager.UserManager()

        self.setupUi(self)

        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.playVideo)
        # self._timer.start(10)
        self.update()

    def setupUi(self, FaceRegister):
        FaceRegister.setObjectName(_fromUtf8("FaceRegister")) #style样式引用
        FaceRegister.resize(800, 640)
        # FaceRegister.center()

        self.inputDialog = InputDialog(self.reciveUserName)
        self.inputDialog.setWindowModality(Qt.ApplicationModal) #阻塞除当前窗体之外的所有的窗体
        self.inputDialog.resize(200,40)
        self.inputDialog.center()
        # self.inputDialog.setGeometry(QtCore.QRect(570, 280, 200, 40))#设置用户名输入窗口位置和大小

        font = QtGui.QFont()
        font.setPointSize(18)
        #顶部文字
        self.label_title = QtGui.QLabel(FaceRegister)
        self.label_title.setGeometry(QtCore.QRect(320, 20, 200, 60))
        self.label_title.setFont(font)
        #进度条
        self.progressBar = QtGui.QProgressBar(FaceRegister)
        self.progressBar.setGeometry(QtCore.QRect(150, 440, 520, 50))
        self.progressBar.setRange(0, 20)
        self.progressBar.setValue(0)
        self.progressBar.setFont(font)
        self.progressBar.setVisible(False)
        #摄像头窗口
        self.video_frame = VideoFrame(FaceRegister)
        self.video_frame.setGeometry(QtCore.QRect(150, 70, 500, 360))
        #底部button
        self.pushButton_capture = QtGui.QPushButton(FaceRegister)
        self.pushButton_capture.setGeometry(QtCore.QRect(200, 520, 100, 60))
        self.pushButton_capture.setFont(font)
        #开始button信号槽
        self.pushButton_capture.clicked.connect(self.pushButton_capture_clicked)

        self.pushButton_back = QtGui.QPushButton(FaceRegister)
        self.pushButton_back.setGeometry(QtCore.QRect(500, 520, 100, 60))
        self.pushButton_back.setFont(font)
        #返回button信号槽
        self.pushButton_back.clicked.connect(self.pushButton_back_clicked)

        self.retranslateUi(FaceRegister)
        QtCore.QMetaObject.connectSlotsByName(FaceRegister)

    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

    def setVideo(self, video):
        self.video = video
        if self.video.is_release:
            self.video.open(0)

    def setModel(self, model):
        self.model = model

    def playVideo(self):
        try:
            pixMap_frame = QtGui.QPixmap.fromImage(self.video.getQImageFrame())
            x = 0;
            y = 0;
            w = 0;
            h = 0
            if self.faceRect is not None:
                x, y, w, h = self.faceRect[0] * 0.8, self.faceRect[1] * 0.75, \
                             self.faceRect[2] * 0.75, self.faceRect[3] * 0.75
            self.video_frame.setRect(x, y, w, h)
            self.video_frame.setPixmap(pixMap_frame)
            self.video_frame.setScaledContents(True) #图片自适应窗口
        except TypeError:
            print('No frame')
    #检测人脸
    def startRec(self):
        self.recognizer = recognize.Recognizer()
        self.recognizer.finished.connect(self.reciveRecognizeResult)
        image = self.video.getGrayCVImage()
        self.recognizer.startRec(image, self.model)
    #获取人脸检测结果
    def reciveRecognizeResult(self):
        self.faceRect = self.recognizer.result
        if self.faceRect is not None and self.captureFlag != 0:
            x, y, w, h = self.faceRect
            crop = face.crop(self.recognizer.faceImage, x, y, w, h)
            personDir = os.path.join(config.FACES_DIR, self.personName)
            if not os.path.exists(personDir):
                os.makedirs(personDir)
            fileName = os.path.join(personDir, 'face_' + '%03d.pgm' % self.captureFlag)
            cv2.imwrite(fileName, face.resize(crop))
            self.captureFlag -= 1
            self.progressBar.setValue(20 - self.captureFlag)
            if self.captureFlag == 0: #获取人脸图片结束
                self.recOver = True
                self.video.release()
                self.startPictureSelect()

        if not self.video.is_release and self.recOver == False:
            self.startRec()

    def reciveUserName(self, name):
        self.personName = str(name.strip())
        if self.Chinese(self.personName):
            self.personName = self.manager.addZhUser(self.personName)
            if not self.personName:
                self.inputDialog.seterrMsg('用户已存在!')
                return
        personDir = os.path.join(config.FACES_DIR, self.personName)
        # self.inputDialog.deleteLater()
        if self.personName=='':
            self.inputDialog.seterrMsg('用户名不能为空!')
        elif os.path.exists(personDir):
            self.inputDialog.seterrMsg('用户已存在!')

        else:
            self.inputDialog.close() #用户不存在则关闭该窗口
            self.pushButton_capture.setEnabled(False)
            self.captureFlag = 20 #获取20张人脸图片
            self.progressBar.setVisible(True) #显示进度条
            # self.label_title.setText('录入人脸信息')
            self._timer.start(10)
            self.startRec()

    #判断中文用户名
    def Chinese(self,chinese_str):
        zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
        # 一个小应用，判断一段文本中是否包含简体中：
        match = zhPattern.search(chinese_str)
        if match:
            return True
        else:
            return False


    def startPictureSelect(self):
        pictureSelect = PictureSelect(self.mainWindow, self.personName)
        pictureSelect.setModel(self.model)
        self.mainWindow.setCentralWidget(pictureSelect)

    def pushButton_capture_clicked(self):
        self.inputDialog.setInfo('请输入用户名')
        self.inputDialog.clear()#清空内容
        self.inputDialog.show()

    def pushButton_back_clicked(self):
        # self._timer.stop()
        self.video.release()
        self.mainWindow.setupUi(self.mainWindow)

    def retranslateUi(self, FaceRegister):
        FaceRegister.setWindowTitle(_translate("FaceRegister", "Form", None))
        self.label_title.setText(_translate("FaceRegister", "录入人脸信息", None))
        self.video_frame.setText(_translate("FaceRegister", " ", None))
        self.pushButton_capture.setText(_translate("FaceRegister", "开始", None))
        self.pushButton_back.setText(_translate("FaceRegister", "返回", None))

#人脸识别界面
class FaceRec(QWidget):
    
    model = None
    confidence = -1
    label = ''
    faceRect = None
    k=0 #计数识别不出的人脸
    # captureFlag = 0
    
    confidences = []
    userInfo = {}

    def __init__(self, mainWindow):
        super(FaceRec, self).__init__()
        self.mainWindow = mainWindow
        self.manager = userManager.UserManager()
        
        self.setupUi(self)
        
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.playVideo)
        self._timer.start(10)
        self.update()
    
    def setModel(self, model):
        self.model = model
    
    def setupUi(self, FaceRec):
        FaceRec.setObjectName(_fromUtf8("FaceRec"))
        FaceRec.resize(800, 640)
        
        font = QtGui.QFont()
        font.setPointSize(16)

        self.label_title = QtGui.QLabel(FaceRec)
        self.label_title.setGeometry(QtCore.QRect(350, 10, 200, 50))
        self.label_title.setFont(font)
        
        self.video_frame = VideoFrame(FaceRec)
        self.video_frame.setGeometry(QtCore.QRect(150, 80, 500, 360))

        self.label_info = QtGui.QLabel(FaceRec)
        self.label_info.setGeometry(QtCore.QRect(220, 430, 500, 50))
        self.label_info.setFont(font)
        
        self.pushButton_back = QtGui.QPushButton(FaceRec)
        self.pushButton_back.setGeometry(QtCore.QRect(350, 520, 100, 50))
        self.pushButton_back.setFont(font)
        self.pushButton_back.clicked.connect(self.pushButton_back_clicked)


        self.retranslateUi(FaceRec)
        QtCore.QMetaObject.connectSlotsByName(FaceRec)

    # def pushButton_capture_clicked(self):
    #     print('capture clicked')
    #     self.captureFlag = 10

    def pushButton_back_clicked(self):
        self._timer.stop()
        self.vs.stop()
        self.video.release()
        self.mainWindow.setupUi(self.mainWindow)

    # def pushButton_capture_clicked(self):
    #     self.startRec()

    def setVideo(self, video):
        self.video = video
        
        self.vs = VideoStream.VideoStream(self.video,'192.168.1.113', 8888)
        #self.vs.startStream()
        self.confidences.clear()
        self.userInfo.clear()
        self.k=0
        self.startRec()
        
    def playVideo(self):
        try:
            pixMap_frame = QtGui.QPixmap.fromImage(self.video.getQImageFrame())
            x = 0;y = 0;w = 0;h = 0
            if self.faceRect is not None:
                #640x480 to 480x360
                x, y, w, h = self.faceRect[0]*0.8, self.faceRect[1]*0.75, self.faceRect[2]*0.75, self.faceRect[3]*0.75
            self.video_frame.setRect(x, y, w, h)
            self.video_frame.setPixmap(pixMap_frame)
            self.video_frame.setScaledContents(True)
        except TypeError:
            print("No frame")
            
    def startRec(self):
        self.recognizer = recognize.Recognizer()
        self.recognizer.finished.connect(self.reciveRecognizeResult)
        image = self.video.getGrayCVImage()
        self.recognizer.startRec(image, self.model)
        
    def reciveRecognizeResult(self):
        self.faceRect = self.recognizer.result
        userName = None
        if not self.video.is_release:
            if self.faceRect is not None:
                if self.recognizer.confidence is not None:
                    self.confidences.append(self.recognizer.confidence)
                    print(self.confidences)
                    mean = sum(self.confidences) / float(len(self.confidences))
                    print('label:',self.recognizer.label)
                    print('confidence: %.4f'%self.recognizer.confidence,'mean:%.4f'%mean)

                    user = self.manager.getUserById(self.recognizer.label)

                    self.video_frame.setUserLabel(userName)

                    if user is not None:
                        userName = user['userName']
                        if 'zh_' in userName:  #中文名
                            userName = self.manager.getZhNamebyEngName(userName)
                        if not userName in self.userInfo.keys():
                            self.userInfo[userName]=1
                        else:
                            self.userInfo[userName]+=1
                    if self.recognizer.confidence <= 60:
                        self.video_frame.setRectColor(0, 255, 0)
                    else:
                        self.video_frame.setRectColor(255, 0, 0)
                else:
                    self.k+=1
            info = 'user: ' + str(userName) + ' <b>|</b> confidence: ' + str(self.recognizer.confidence)
            self.label_info.setText(info)
            if len(self.confidences)>=20:
                self.userInfo = sorted(self.userInfo.items(),key=lambda x:x[1],reverse=True)
                nameRes = self.userInfo[0][0]
                info_str = '识别结果:  %s  ' % nameRes
                self.recFinished(info_str)
            elif self.k>=50:
                info_str = '无法识别当前人脸!'
                self.recFinished(info_str)
            else:
                self.startRec()

    def recFinished(self,info_str):
        dialog = QtGui.QMessageBox()
        dialog.setWindowTitle('info')
        dialog.setWindowModality(Qt.ApplicationModal)  #
        dialog.setFixedSize(300,300)
        font = QtGui.QFont()
        font.setPointSize(15)
        dialog.setFont(font)
        dialog.setText(info_str)
        if dialog.exec_():
            self.pushButton_back_clicked()


    def retranslateUi(self, FaceRec):
        FaceRec.setWindowTitle(_translate("FaceRec", "from", None))
        self.label_title.setText(_translate("FaceRec", "人脸识别", None))
        self.video_frame.setText(_translate("FaceRec", "video_frame", None))
        self.label_info.setText(_translate("FaceRec", "label_info", None))
        self.pushButton_back.setText(_translate("FaceRec", "返回", None))

#删除人脸
class DelFace(QWidget):

    faceNames = []
    model = None

    def __init__(self,mainWindow):
        super(DelFace, self).__init__()
        self.mainWindow = mainWindow
        self.manager = userManager.UserManager()
        self.data = self.manager.getAllUser() #csv文件数据
        self.zhData = self.manager.getAllZhUser() #中文用户csv数据

        self.zhUserName = self.manager.getAllZhUserEngName()

        self.setupUi(self)
        self.readFaces()
        self.showFaces()

        self._timer = QtCore.QTimer(self)
        self._timer.start(10)
        self.update()

    def setupUi(self,DelFace):
        DelFace.setObjectName(_fromUtf8("DelFace"))  # style样式引用
        DelFace.resize(800, 640)

        font = QtGui.QFont()
        font.setPointSize(18)

        self.label_info = QtGui.QLabel(DelFace)
        self.label_info.setGeometry(QtCore.QRect(160, 20, 480, 50))
        self.label_info.setFont(font)

        self.scrollArea = QtGui.QScrollArea(DelFace)
        self.scrollArea.setGeometry(QtCore.QRect(150, 80, 500, 400))  # 图片窗口
        self.scrollArea.setWidgetResizable(False)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        # self.scrollAreaWidgetContents = QtGui.QWidget()
        # self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 600, 548))

        self.gridLayoutWidget = QtGui.QWidget(self.scrollArea)

        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)

        self.scrollArea.setWidget(self.gridLayoutWidget)

        font = QtGui.QFont()
        font.setPointSize(16)

        self.pushButton_delete = QtGui.QPushButton(DelFace)
        self.pushButton_delete.setGeometry(QtCore.QRect(200, 520, 100, 60))
        self.pushButton_delete.setFont(font)
        self.pushButton_delete.clicked.connect(self.pushButton_delete_clicked)

        self.pushButton_back = QtGui.QPushButton(DelFace)
        self.pushButton_back.setGeometry(QtCore.QRect(500, 520, 100, 60))
        self.pushButton_back.setFont(font)
        self.pushButton_back.setObjectName(_fromUtf8("pushButton_back"))
        self.pushButton_back.clicked.connect(self.pushButton_back_clicked)

        self.retranslateUi(DelFace)
        QtCore.QMetaObject.connectSlotsByName(DelFace)

    def setModel(self,model):
        self.model = model
    def readFaces(self):
        self.faceNames = []
        path = config.FACES_DIR
        for dirName in train.walkDirs(path):
            faceName = dirName.split('faces\\')[1] #人脸名
            self.faceNames.append(faceName)


    def clearGridLayout(self):
        for i in reversed(list(range(self.gridLayout.count()))):
            self.gridLayout.itemAt(i).widget().deleteLater()

    def showFaces(self):
        for i in range(0, len(self.faceNames)):
            if self.faceNames[i] in self.zhUserName:
                self.faceNames[i] = self.manager.getZhNamebyEngName(self.faceNames[i])
            font = QtGui.QFont()
            font.setPointSize(16)

            pe = QPalette()  # 设置提示信息颜色
            pe.setColor(QPalette.WindowText, Qt.blue)
            self.checkbox = QCheckBox(self.faceNames[i],self)
            self.checkbox.setFocusPolicy(QtCore.Qt.NoFocus)
            self.checkbox.setFont(font)
            self.checkbox.setPalette(pe)
            # self.checkbox.setObjectName("box_%d"%i)
            self.checkbox.setFixedSize(165,30)
            # checkbox.toggle() #默认选中
            # self.connect(self.checkbox, QtCore.SIGNAL('stateChanged(int)'), self.changeColor("box_%d"%i))
            self.gridLayout.addWidget(self.checkbox, i / 3, i % 3, 1, 1)
            self.gridLayoutWidget.setFixedSize(self.gridLayout.sizeHint())

    def pushButton_delete_clicked(self):
        self.pushButton_delete.setEnabled(False)
        for i in range(self.gridLayout.count()):
            item = self.gridLayout.itemAt(i)
            if item is not None:
                checkbox = item.widget()
                # print(label_pic.pictureName)
                if checkbox.isChecked():
                    self.delFaceData(checkbox.text())
        #删除完成 重写csv 重新训练模型 重新加载面板
        self.delFinished("完成人脸删除")
        self.clearGridLayout() #清空checkbox
        self.readFaces()
        self.showFaces()
        self.pushButton_delete.setEnabled(True)

    #处理删除人脸文件和CSV数据
    def delFaceData(self,facename):
        if facename in self.manager.getAllZhUserZhName():
            facename = self.manager.getEngNamebyZhName(facename)
            for i in range(0, len(self.zhData)):
                if self.zhData[i]['EngName'] == facename:
                    del self.zhData[i]
                    break
        shutil.rmtree(os.path.join(config.FACES_DIR, facename))  # 删除目录
        print(facename,"目录已删除")
        for i in range(0,len(self.data)):
            if self.data[i]['userName'] == facename:
                del self.data[i]
                break

    def delFinished(self,info_str):
        self.manager.writeCSV(self.data)
        self.manager.writeZhCSV(self.zhData)
        train.trainFace(self.model)
        dialog = QtGui.QMessageBox()
        dialog.setWindowTitle('info')
        dialog.setWindowModality(Qt.ApplicationModal)  #
        dialog.setFixedSize(300,300)
        font = QtGui.QFont()
        font.setPointSize(15)
        dialog.setFont(font)
        dialog.setText(info_str)
        if dialog.exec_():
            pass
            # self.pushButton_back_clicked()

    def pushButton_back_clicked(self):
        self.gridLayout = None
        self.pictures = []
        self.pictureNames = []
        self.destroy()
        self.mainWindow.setupUi(self.mainWindow)

    def retranslateUi(self, DelFace):
        DelFace.setWindowTitle(_translate("DelFace", "Form", None))
        self.label_info.setText(_translate("DelFace", "删除人脸", None))
        self.pushButton_back.setText(_translate("DelFace", "返回", None))
        self.pushButton_delete.setText(_translate("DelFace", "删除", None))

#用户名输入控件
class InputDialog(QWidget):
    def __init__(self, callback):
        QWidget.__init__(self)
        
        self.callback = callback

        font = QtGui.QFont()
        font.setPointSize(11)

        self.labelInfo = QtGui.QLabel()
        self.labelInfo.setFont(font)

        self.msgInfo = QtGui.QLabel()
        pe = QPalette() #设置提示信息颜色
        pe.setColor(QPalette.WindowText, Qt.red)
        self.msgInfo.setPalette(pe)
        self.msgInfo.setFont(font)


        self.editUserName = QtGui.QLineEdit()
        self.editUserName.setFont(font)
        # self.editUserName.keyboard_type = 'default'
        
        self.pushButton_accept = QtGui.QPushButton(self)
        self.pushButton_accept.setText('确认')
        self.pushButton_accept.setFont(font)
        self.pushButton_accept.clicked.connect(self.reciveUserName)


        gl = QtGui.QVBoxLayout()
        gl.addWidget(self.labelInfo)
        gl.addWidget(self.editUserName)
        gl.addWidget(self.pushButton_accept)
        gl.addWidget(self.msgInfo)

        
        self.setLayout(gl)

    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

    def setInfo(self, info):
        self.labelInfo.setText(info)

    def seterrMsg(self,info):
        self.msgInfo.setText(info)

    def clear(self):
        self.editUserName.clear()
        self.msgInfo.clear()
        
    def reciveUserName(self):
        # self.touch_interface._input_panel_all.hide()
        self.userName = self.editUserName.text()
        # if self.userName == '':
        #     return
        self.callback(self.userName)
        # self.hide()

#图片选择界面
class PictureSelect(QWidget):
    
    pictures = []
    pictureNames = []
    path = None
    model = None

    def __init__(self, mainWindow, path):
        super(PictureSelect, self).__init__()
        self.mainWindow = mainWindow
        self.path = path

        self.setupUi(self)
        
        self.readPictures()
        
        self.showPictures()
        
    def setupUi(self, pictureSelect):
        pictureSelect.setObjectName(_fromUtf8("pictureSelect"))
        # pictureSelect.resize(800, 640)
        
        # self.setStyleSheet(style)
        
        font = QtGui.QFont()
        font.setPointSize(18)

        self.label_info = QtGui.QLabel(pictureSelect)
        self.label_info.setGeometry(QtCore.QRect(160, 20, 480, 50))
        self.label_info.setFont(font)

        self.scrollArea = QtGui.QScrollArea(pictureSelect)
        self.scrollArea.setGeometry(QtCore.QRect(135, 80, 530, 400)) #图片窗口
        self.scrollArea.setWidgetResizable(False)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 600, 548))

        self.gridLayoutWidget = QtGui.QWidget(self.scrollArea)
        
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        
        self.scrollArea.setWidget(self.gridLayoutWidget)
        
        font = QtGui.QFont()
        font.setPointSize(16)
        
        self.pushButton_delete = QtGui.QPushButton(pictureSelect)
        self.pushButton_delete.setGeometry(QtCore.QRect(200, 520, 100, 60))
        self.pushButton_delete.setFont(font)
        self.pushButton_delete.clicked.connect(self.pushButton_delete_clicked)
        
        self.pushButton_ok = QtGui.QPushButton(pictureSelect)
        self.pushButton_ok.setGeometry(QtCore.QRect(350, 520, 100, 60))
        self.pushButton_ok.setFont(font)
        self.pushButton_ok.clicked.connect(self.pushButton_ok_clicked)
        
        self.pushButton_back = QtGui.QPushButton(pictureSelect)
        self.pushButton_back.setGeometry(QtCore.QRect(500, 520, 100, 60))
        self.pushButton_back.setFont(font)
        self.pushButton_back.setObjectName(_fromUtf8("pushButton_back"))
        self.pushButton_back.clicked.connect(self.pushButton_back_clicked)

        self.retranslateUi(pictureSelect)
        QtCore.QMetaObject.connectSlotsByName(pictureSelect)

    def setModel(self, model):
        self.model = model

    def readPictures(self):
        self.pictures = []
        self.pictureNames = []
        path = os.path.join(config.FACES_DIR, self.path)
        for fileName in train.walkFiles(path, '*.pgm'):
            self.pictures.append(QtGui.QPixmap(fileName))
            self.pictureNames.append(fileName)

    def clearGridLayout(self):
        for i in reversed(list(range(self.gridLayout.count()))):
            self.gridLayout.itemAt(i).widget().deleteLater()

    def showPictures(self):
        for i in range(0, len(self.pictures)):
            label_pic = PictureLabel()
            label_pic.mousePressEvent = label_pic.clicked
            h = self.pictures[i].height()
            w = self.pictures[i].width()
            label_pic.setFixedSize(QSize(w, h))
            label_pic.setPixmap(self.pictures[i])
            label_pic.setPictureName(self.pictureNames[i])
            self.gridLayout.addWidget(label_pic, i/5, i%5, 1, 1) #设置图片选择窗口每行显示5张
        self.gridLayoutWidget.setFixedSize(self.gridLayout.sizeHint())

    def trainFinish(self):
        dialog = QtGui.QMessageBox()
        dialog.setWindowTitle('info')
        dialog.setWindowModality(Qt.ApplicationModal) #阻塞其他窗口
        font = QtGui.QFont()
        font.setPointSize(11)
        dialog.setFont(font)
        dialog.setText('人脸录入已完成(%s)'%self.path)
        if dialog.exec_():
            self.label_info.setText('选择要删除的图片，点击删除按钮进行删除')
            self.pushButton_ok.setEnabled(True)

    def pushButton_delete_clicked(self):
        self.pushButton_delete.setEnabled(False)
        for i in range(self.gridLayout.count()):
            item = self.gridLayout.itemAt(i)
            if item is not None:
                label_pic = item.widget()
                # print(label_pic.pictureName)
                if label_pic.selected:
                    print('delete',label_pic.pictureName)
                    os.remove(os.path.join(config.FACES_DIR, self.path, label_pic.pictureName))
            
        self.clearGridLayout()   
        self.readPictures()
        self.showPictures()
        self.pushButton_delete.setEnabled(True)

    def pushButton_ok_clicked(self):
        self.label_info.setText('正在录入人脸...')
        self.pushButton_ok.setEnabled(False)
        self.trainThread = TrainThread(self.model, os.path.join(config.TRAINING_DIR, config.TRAINING_FILE))
        self.trainThread.finished.connect(self.trainFinish)
        self.trainThread.start()

    def pushButton_back_clicked(self):
        self.gridLayout = None
        self.pictures = []
        self.pictureNames = []
        self.mainWindow.setupUi(self.mainWindow)

    def retranslateUi(self, pictureSelect):
        pictureSelect.setWindowTitle(_translate("pictureSelect", "Form", None))
        self.label_info.setText(_translate("pictureSelect", "选择要删除的图片，点击删除按钮进行删除", None))
        self.pushButton_back.setText(_translate("pictureSelect", "返回", None))
        self.pushButton_delete.setText(_translate("pictureSelect", "删除", None))
        self.pushButton_ok.setText(_translate("pictureSelect", "录入", None))

class TrainThread(QtCore.QThread):
    
    model = None
    trainFileName = None
    
    def __init__(self, model, trainFileName):
        super(TrainThread, self).__init__()
        
        self.model = model
        self.trainFileName = trainFileName
        
    def run(self):
        train.trainFace(self.model)
        print('人脸训练完毕')
        self.model.load(self.trainFileName)
        print('模型加载完毕')

#复选框

#显示单个图像的Qt控件
class PictureLabel(QtGui.QLabel):
        
    selected = False
    pictureName = None
    
    def __init__(self):
        QtGui.QLabel.__init__(self)
        self.deleteImage = QtGui.QPixmap('./res/pic/delete_100x100.png')
        
    def setPictureName(self, name):
        self.pictureName = name
        
    def clicked(self, event):
        if self.selected:
            self.selected = False
        else:
            self.selected = True
        self.update()
        
    def paintEvent(self, event):
        QtGui.QLabel.paintEvent(self,event)
        if self.selected:
            painter = QtGui.QPainter(self)
            size = self.sizeHint()
            x = size.width()/2 - 50
            y = size.height()/2 - 50
            painter.drawPixmap(x, y, self.deleteImage)
