#!/usr/bin/env python
#  -- coding:utf-8 --
# #@Time  : 2017/3/22
# #@Author: Jee
import datetime
from time import strftime
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from . import ui

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

style = open('./ui/css/style.css').read()

class Ui_MainWindow(QMainWindow):
    model = None
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        
        self.setupUi(self)
        # self.setStyleSheet(style)
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 640)
        # 禁止最大化按钮
        # MainWindow.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
        # 禁止拉伸窗口大小
        MainWindow.setFixedSize(MainWindow.width(), MainWindow.height());
        # MainWindow.showFullScreen()
        
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

        #按钮（垂直布局）
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)

        self.label_welcome = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(32)
        self.label_welcome.setFont(font)
        self.label_welcome.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.label_welcome)

        self.gridLayout_buttons = QtGui.QGridLayout()
        self.gridLayout_buttons.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.gridLayout_buttons.setMargin(0) #控件与窗口左右边距
        self.gridLayout_buttons.setSpacing(50) #各个控件之间的上下间距

        #button控件自适应策略
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum) #不能再缩小
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        #人脸录入button
        self.btn_register = QtGui.QPushButton(self.centralwidget)
        sizePolicy.setHeightForWidth(self.btn_register.sizePolicy().hasHeightForWidth())# 首选Height取决于width
        self.btn_register.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(26)
        self.btn_register.setFont(font)
        # self.btn_register.setMaximumWidth(200)
        self.gridLayout_buttons.addWidget(self.btn_register, 0, 0, 1, 1) #（行，列，占用行数，占用列数）
        #button人脸录入信号槽
        self.btn_register.clicked.connect(self.btn_register_clicked)

        # 人脸识别button
        self.btn_face = QtGui.QPushButton(self.centralwidget)
        sizePolicy.setHeightForWidth(self.btn_face.sizePolicy().hasHeightForWidth())  # 首选Height取决于width
        self.btn_face.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(26)
        self.btn_face.setFont(font)
        self.gridLayout_buttons.addWidget(self.btn_face, 1, 0, 1, 1)
        # button人脸识别信号槽
        self.btn_face.clicked.connect(self.btn_face_clicked)

        # 退出button
        self.btn_exit = QtGui.QPushButton(self.centralwidget)
        sizePolicy.setHeightForWidth(self.btn_exit.sizePolicy().hasHeightForWidth())
        self.btn_exit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(26)
        self.btn_exit.setFont(font)
        self.gridLayout_buttons.addWidget(self.btn_exit, 2, 0, 1, 1)
        #button退出信号槽
        self.btn_exit.clicked.connect(self.btn_exit_clicked)

        self.verticalLayout.addLayout(self.gridLayout_buttons)

        #底部显示
        self.horizontallayout = QtGui.QHBoxLayout()  # 00

        self.author = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.author.setFont(font)
        self.horizontallayout.addWidget(self.author)  # 00
        # self.horizontallayout.addStretch(1)

        self.label_date = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_date.setFont(font)
        self.horizontallayout.addWidget(self.label_date)  # 00

        self.lcd_time = QtGui.QLCDNumber(self.centralwidget)
        # font = QtGui.QFont()
        # font.setPointSize(20)
        # self.lcd_time.setFont(font)
        # pe = QPalette()  # 设置提示信息颜色
        # pe.setColor(QPalette.WindowText, Qt.red)
        # self.lcd_time.setPalette(pe)
        self.lcd_time.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))  # set cursor style
        self.lcd_time.setDigitCount(8)  # 设置LCD显示位数
        self.lcd_time.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lcd_time.setLineWidth(0)  # 无边框
        self.horizontallayout.addWidget(self.lcd_time) # 00
        self.horizontallayout.setContentsMargins(10,35,0,0) #左 上 右 下
        # self.verticalLayout.addStretch(1)
        self.verticalLayout.addLayout(self.horizontallayout)

        #vbox占比分配
        self.verticalLayout.setStretch(0, 2)  #welcome_label
        self.verticalLayout.setStretch(1, 5)  #gridLayout_buttons
        self.verticalLayout.setStretch(2, 1)  # horizontallayout

        MainWindow.setCentralWidget(self.centralwidget) #中心窗口
        exit = QtGui.QAction(QtGui.QIcon('icons/exit.png'), 'Exit', self)
        exit.setShortcut('Ctrl+Q')
        exit.setStatusTip('Exit application')
        self.connect(exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))

        self.menubar = QtGui.QMenuBar(MainWindow) #菜单栏
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menubar.addMenu('&Exit').addAction(exit)
        MainWindow.setMenuBar(self.menubar)

        # 状态栏
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #刷新显示时间
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.updateTime)
        self._timer.start(1000)
        self.update()

    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        print(size.width()," ",size.height)
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def updateTime(self):
        # date = datetime.datetime.now().strftime('    %Y-%m-%d')
        dateNow = datetime.datetime.now()
        dy = dateNow.strftime('     %Y')
        dm = dateNow.strftime('%m')
        dd = dateNow.strftime('%d')
        time = dateNow.strftime('%H:%M:%S')
        
        self.label_date.setText(dy+'年'+dm+'月'+dd+'日')
        # self.lcd_time.setText(time)
        self.lcd_time.display(strftime("%H"+":"+"%M"+":"+"%S"))

    def setModel(self, model):
        self.model = model

    def setVideo(self, video):
        self.video = video
    #人脸识别button
    def btn_face_clicked(self):
        # print('facerec clicked')
        self.video.open(0)
        self._timer.stop()
        
        self.facerec = ui.FaceRec(self)
        self.facerec.setModel(self.model)
        self.facerec.setVideo(self.video)
        self.setCentralWidget(self.facerec)
    #人脸录入button
    def btn_register_clicked(self):
        self._timer.stop()
        
        self.register = ui.FaceRegister(self)
        self.register.setModel(self.model)
        self.register.setVideo(self.video)
        self.setCentralWidget(self.register)
    #退出button
    def btn_exit_clicked(self):
        exit(1)
    #设置控件内容
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "人脸识别系统", None))
        self.label_date.setText(_translate("MainWindow", "    0000年00月00日", None))
        self.label_welcome.setText(str("人脸识别系统"))
        self.btn_register.setText("人脸录入")
        self.btn_face.setText("人脸识别")
        self.btn_exit.setText("退出")
        self.author.setText("Author:Jee")

