# @Time    : 2019/12/17 19:20
# @Author  : Dreambee
# @File    : WorkThread.py
# @Software: PyCharm
# @Desciption: 多线程展现video_label
import cv2
from PyQt5.QtCore import QThread, QTimer
from PyQt5.QtGui import QImage, QPixmap


class WorkThread(QThread):
    def __init__(self, ezapi, device_no, video_label):
        super(WorkThread, self).__init__()
        # self.url = ezapi.get_live_url(device_no=device_no)
        self.url = "rtmp://rtmp01open.ys7.com/openlive/e468865941be470d9a0a36a9a4b92ebf.hd"
        self.timer = QTimer()
        self.timer.start(1)
        self.camera_api = ezapi
        self.device_no = device_no
        self.video_label = video_label
        self.token = True
        self.cap = cv2.VideoCapture(self.url)

    def run(self):
        self.timer.timeout.connect(self.frame)

    def frame(self):
        ret, frame = self.cap.read()
        if ret:
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)
            self.video_label.setPixmap(QPixmap.fromImage(img))
