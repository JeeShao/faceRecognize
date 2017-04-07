from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.setGeometry(300, 300, 300, 220)

        self.center()

        self.setWindowTitle('窗口居中')
        self.show()

    def position(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        print(size.width()," ",size.height)
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
