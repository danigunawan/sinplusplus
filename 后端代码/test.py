# @Time    : 2019/12/17 19:44
# @Author  : Dreambee
# @File    : test.py
# @Software: PyCharm
# @Desciption:
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.t = 0

        window = QWidget()
        vbox = QVBoxLayout(window)
        # vbox = QVBoxLayout(window)

        lcdNumber = QLCDNumber()
        button = QPushButton("测试")
        vbox.addWidget(lcdNumber)
        vbox.addWidget(button)

        self.timer = QTimer()

        button.clicked.connect(self.work)
        self.timer.timeout.connect(self.setTime)

        self.setLayout(vbox)
        self.show()

    def setTime(self):
        self.t += 1
        self.lcdNumber.display(self.t)

    def work(self):
        self.timer.start(10000)
        for i in range(200000000):
            pass
        self.timer.stop()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    th = Example()
    sys.exit(app.exec_())
