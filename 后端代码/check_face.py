# @Time    : 2019/12/30 11:54
# @Author  : Dreambee
# @File    : check_face.py
# @Software: PyCharm
# @Desciption: 输入一张图片，提取其中人脸特征，加入facebank中
import os

import cv2
from PIL import Image
import numpy as np

from lib.InsightFace.mtcnn import MTCNN
from datetime import datetime


def store_face(img, mtcnn, name):
    save_path = 'lib/InsightFace/data/facebank/' + name
    os.makedirs(save_path, exist_ok=True)
    p = Image.fromarray(img[..., ::-1])
    try:
        warped_face = np.array(mtcnn.align(p))[..., ::-1]
        cv2.imwrite(str(save_path + '/' + '{}.jpg'.format(str(datetime.now())[:-7].replace(":", "-").replace(" ", "-"))),
                    warped_face)
    except Exception as e:
        print(e)
        return False
    return True


if __name__ == "__main__":
    img = cv2.imread("")
    mtcnn = MTCNN()
    name = "qz"
    store_face(img, mtcnn, name)
