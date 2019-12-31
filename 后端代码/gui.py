# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1124, 866)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.video_label = QtWidgets.QLabel(self.centralwidget)
        self.video_label.setGeometry(QtCore.QRect(70, 40, 531, 341))
        self.video_label.setObjectName("video_label")
        self.picture_label = QtWidgets.QLabel(self.centralwidget)
        self.picture_label.setGeometry(QtCore.QRect(70, 420, 534, 341))
        self.picture_label.setObjectName("picture_label")
        self.capture_btn = QtWidgets.QPushButton(self.centralwidget)
        self.capture_btn.setGeometry(QtCore.QRect(890, 550, 151, 81))
        self.capture_btn.setObjectName("capture_btn")
        self.recog_tbl = QtWidgets.QTableWidget(self.centralwidget)
        self.recog_tbl.setEnabled(True)
        self.recog_tbl.setGeometry(QtCore.QRect(640, 30, 441, 381))
        self.recog_tbl.setGridStyle(QtCore.Qt.SolidLine)
        self.recog_tbl.setObjectName("recog_tbl")
        self.recog_tbl.setColumnCount(0)
        self.recog_tbl.setRowCount(0)
        self.exit_btn = QtWidgets.QPushButton(self.centralwidget)
        self.exit_btn.setGeometry(QtCore.QRect(680, 660, 361, 81))
        self.exit_btn.setObjectName("exit_btn")
        self.connect_btn = QtWidgets.QPushButton(self.centralwidget)
        self.connect_btn.setGeometry(QtCore.QRect(680, 550, 151, 81))
        self.connect_btn.setObjectName("connect_btn")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1124, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.video_label.setText(_translate("MainWindow", "设备未连接"))
        self.picture_label.setText(_translate("MainWindow", "未捕获到任何图片"))
        self.capture_btn.setToolTip(_translate("MainWindow", "<html><head/><body><p>捕获视频中的当前帧</p></body></html>"))
        self.capture_btn.setText(_translate("MainWindow", "Capture"))
        self.recog_tbl.setSortingEnabled(False)
        self.exit_btn.setToolTip(_translate("MainWindow", "<html><head/><body><p>退出应用</p></body></html>"))
        self.exit_btn.setText(_translate("MainWindow", "Exit"))
        self.connect_btn.setToolTip(_translate("MainWindow", "<html><head/><body><p>捕获视频中的当前帧</p></body></html>"))
        self.connect_btn.setText(_translate("MainWindow", "Connect"))
