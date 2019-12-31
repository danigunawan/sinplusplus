# @Time    : 2019/12/15 14:16
# @Author  : Dreambee
# @File    : gui-pyqt.py
# @Software: PyCharm
# @Desciption:
import sys

import cv2
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer, QCoreApplication
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView

from WorkThread import WorkThread
from connection import ConThread
from gui import Ui_MainWindow
from lib.InsightFace.Learner import face_learner
from lib.InsightFace.config import get_config
from lib.InsightFace.face_verify import recognize
from lib.InsightFace.mtcnn import MTCNN
from lib.InsightFace.utils import load_facebank
from lib.cloud.ezapi import EZAPI


class SinApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(SinApp, self).__init__(parent)
        self.setupUi(self)
        self.device_no = None
        self.capture_btn.clicked.connect(self.capture)
        self.video_label.setScaledContents(True)
        self.picture_label.setScaledContents(True)
        # self.cap = cv2.VideoCapture(0)
        # self.timer_camera.timeout.connect(self.show_vid)

        # Load recognition module
        self.mtcnn = MTCNN()
        self.conf = get_config(False)
        self.targets, self.names = load_facebank(self.conf)
        self.learner = face_learner(self.conf, True)
        if self.conf.device.type == 'cpu':
            self.learner.load_state(self.conf, 'cpu_final.pth', True, True)
        else:
            self.learner.load_state(self.conf, 'final.pth', True, True)
        self.learner.model.eval()

        # 表格
        self.recog_tbl.setRowCount(15)
        self.recog_tbl.setColumnCount(2)
        self.recog_tbl.setHorizontalHeaderLabels(['学号', '姓名'])
        self.recog_tbl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 自适应伸缩

        # 退出
        self.exit_btn.clicked.connect(self.exit)

        # 对接萤石云
        self.camera_api = EZAPI()
        self.connect_btn.clicked.connect(self.connect)
        self.device_no = self.camera_api.connect_device()

        # 多线程
        self.vid_thread = WorkThread(self.camera_api, self.device_no, self.video_label)

        # 多线程相应快应用capture请求
        self.con_thread = ConThread(self.device_no, self.mtcnn, self.targets, self.names, self.learner, self.conf)
        self.con_thread.start()

    def connect(self):
        """
        当点击按钮时，链接远端摄像头，将图片显示在video中
        :return:
        """
        self.vid_thread.start()

    def capture(self):
        frame = self.camera_api.capture_picture(self.device_no)
        self.recog_tbl.clearContents()
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        try:
            img, names = recognize(img, self.mtcnn, self.targets, self.names, self.learner, self.conf)
            img = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)
            self.picture_label.setPixmap(QPixmap.fromImage(img))
            for count, name in enumerate(names):
                self.recog_tbl.setItem(count, 0, QTableWidgetItem(str(count+1)))
                self.recog_tbl.setItem(count, 1, QTableWidgetItem(name))
        except BaseException as err:
            # 有时候识别不到人脸
            print(err)

    def exit(self):
        QCoreApplication.instance().quit()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = SinApp()
    window.show()
    window.vid_thread.wait()
    sys.exit(app.exec_())
