"""
@time:      2019-12-09 10:03:06
@version:   v1.0
@author：   hujunchina@outlook.com
"""
import cv2

from lib.cloud.log import Log
import requests
import os
import numpy as np


class EZAPI(object):
    appKey = None
    appSecret = None
    appToken = None
    log = None

    # 初始化
    def __init__(self, app_key=None, app_secret=None):
        self.log = Log()
        if app_key is None:
            self.appKey = "c127ab47d5dc450088b7c9ce8a8aac85"
            self.log.warning("app key is none")
        else:
            self.appKey = app_key
        if app_secret is None:
            self.appSecret = "9316c6d3ece1d67e7eb8b386fb365fb5"
            self.log.warning("app secret is none")
        else:
            self.appSecret = app_secret
        self.log.info("EZAPI started")

    # 请求调用
    def post_request(self, url, params=None):
        return requests.request("POST", url, params=params)

    # 获得token
    def get_token(self):
        params = {'appKey': self.appKey, 'appSecret': self.appSecret}
        url = "https://open.ys7.com/api/lapp/token/get"
        ret = self.post_request(url, params)
        if ret.status_code is not 200:
            self.log.error("request failed with {0}".format(ret.status_code))
            return
        r = ret.json()
        self.appToken = r['data']['accessToken']
        self.log.info("app token is {0}".format(self.appToken))
        return self.appToken

    # 获得相机列表
    def get_camera_list(self, page_start=0, page_size=10):
        params = {'accessToken': self.appToken, 'pageStart':page_start, 'pageSize':page_size}
        url = "https://open.ys7.com/api/lapp/camera/list"
        ret = self.post_request(url, params)
        if ret.status_code is not 200:
            self.log.error("request failed with {0}".format(ret.status_code))
            return
        r = ret.json()
        if r['page']['total'] is 0:
            self.log.error("camera total is 0")
            return
        else:
            return r['data'][0]['deviceSerial']

    def get_live_url(self, device_no=None):
        if device_no is None:
            device_no = self.connect_device()
        params = {'accessToken': self.appToken}
        url = "https://open.ys7.com/api/lapp/live/video/list"
        ret = self.post_request(url, params)
        if ret.status_code is not 200:
            self.log.error("request failed with {0}".format(ret.status_code))
            return
        r = ret.json()
        return r['data'][0]['hdAddress']

    # 截图
    def camera_capture(self, device_serial=None, channel_no=1):
        if device_serial is None:
            self.log.error("device serial is none")
            return
        params = {'accessToken': self.appToken, 'deviceSerial': device_serial, 'channelNo': channel_no}
        url = 'https://open.ys7.com/api/lapp/device/capture'
        ret = self.post_request(url, params)  # 这一步很费时
        if ret.status_code is not 200:
            self.log.error("request failed with {0}".format(ret.status_code))
            return
        r = ret.json()
        # todo: 捕获照片时，获得的picUrl是否是固定的？只与设备号有关？
        return r['data']['picUrl']

    # 保存图片
    def get_camera_picture(self, url, want_img=False):
        r = requests.get(url, stream=True)
        if r.status_code is not 200:
            self.log.error("request failed with {0}".format(r.status_code))
            return
        if r.status_code is 200:
            if want_img:
                return cv2.imdecode(np.frombuffer(r.content, np.uint8), cv2.IMREAD_COLOR)
            pic = "vid.jpg"
            with open(pic, 'wb') as f:
                for chunk in r:
                    f.write(chunk)
            # if want_img:
            #     return cv2.imread(pic)

    def connect_device(self):
        # 链接
        self.get_token()
        devicesSerial = self.get_camera_list()  # str
        return devicesSerial

    def capture_picture(self, device_no, want_img=True):
        # capture
        picURL = self.camera_capture(device_no)
        print(picURL)
        img = self.get_camera_picture(picURL, want_img=want_img)  #
        return img


if __name__ == '__main__':
    ezapi = EZAPI()
    device_no = ezapi.connect_device()
    picture = ezapi.capture_picture(device_no)



