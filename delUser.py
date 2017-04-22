# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\OneDrive\faceRecognize\delUser.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(511, 469)
        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(190, 20, 81, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("黑体"))
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(130, 380, 75, 23))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(320, 380, 75, 23))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.widget = QtGui.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(120, 100, 281, 231))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.checkBox_9 = QtGui.QCheckBox(self.widget)
        self.checkBox_9.setObjectName(_fromUtf8("checkBox_9"))
        self.gridLayout.addWidget(self.checkBox_9, 2, 1, 1, 1)
        self.checkBox_10 = QtGui.QCheckBox(self.widget)
        self.checkBox_10.setObjectName(_fromUtf8("checkBox_10"))
        self.gridLayout.addWidget(self.checkBox_10, 4, 0, 1, 1)
        self.checkBox_6 = QtGui.QCheckBox(self.widget)
        self.checkBox_6.setObjectName(_fromUtf8("checkBox_6"))
        self.gridLayout.addWidget(self.checkBox_6, 4, 1, 1, 1)
        self.checkBox_5 = QtGui.QCheckBox(self.widget)
        self.checkBox_5.setObjectName(_fromUtf8("checkBox_5"))
        self.gridLayout.addWidget(self.checkBox_5, 5, 1, 1, 1)
        self.checkBox_7 = QtGui.QCheckBox(self.widget)
        self.checkBox_7.setObjectName(_fromUtf8("checkBox_7"))
        self.gridLayout.addWidget(self.checkBox_7, 1, 1, 1, 1)
        self.checkBox_8 = QtGui.QCheckBox(self.widget)
        self.checkBox_8.setObjectName(_fromUtf8("checkBox_8"))
        self.gridLayout.addWidget(self.checkBox_8, 0, 1, 1, 1)
        self.checkBox = QtGui.QCheckBox(self.widget)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.gridLayout.addWidget(self.checkBox, 0, 0, 1, 1)
        self.checkBox_2 = QtGui.QCheckBox(self.widget)
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
        self.gridLayout.addWidget(self.checkBox_2, 1, 0, 1, 1)
        self.checkBox_4 = QtGui.QCheckBox(self.widget)
        self.checkBox_4.setObjectName(_fromUtf8("checkBox_4"))
        self.gridLayout.addWidget(self.checkBox_4, 5, 0, 1, 1)
        self.checkBox_3 = QtGui.QCheckBox(self.widget)
        self.checkBox_3.setObjectName(_fromUtf8("checkBox_3"))
        self.gridLayout.addWidget(self.checkBox_3, 2, 0, 1, 1)
        self.checkBox_11 = QtGui.QCheckBox(self.widget)
        self.checkBox_11.setObjectName(_fromUtf8("checkBox_11"))
        self.gridLayout.addWidget(self.checkBox_11, 3, 0, 1, 1)
        self.checkBox_12 = QtGui.QCheckBox(self.widget)
        self.checkBox_12.setObjectName(_fromUtf8("checkBox_12"))
        self.gridLayout.addWidget(self.checkBox_12, 3, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.delete)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label.setText(_translate("Form", "删除人脸", None))
        self.pushButton.setText(_translate("Form", "删除", None))
        self.pushButton_2.setText(_translate("Form", "返回", None))
        self.checkBox_9.setText(_translate("Form", "CheckBox", None))
        self.checkBox_10.setText(_translate("Form", "CheckBox", None))
        self.checkBox_6.setText(_translate("Form", "CheckBox", None))
        self.checkBox_5.setText(_translate("Form", "CheckBox", None))
        self.checkBox_7.setText(_translate("Form", "CheckBox", None))
        self.checkBox_8.setText(_translate("Form", "CheckBox", None))
        self.checkBox.setText(_translate("Form", "CheckBox", None))
        self.checkBox_2.setText(_translate("Form", "CheckBox", None))
        self.checkBox_4.setText(_translate("Form", "CheckBox", None))
        self.checkBox_3.setText(_translate("Form", "CheckBox", None))
        self.checkBox_11.setText(_translate("Form", "CheckBox", None))
        self.checkBox_12.setText(_translate("Form", "CheckBox", None))

