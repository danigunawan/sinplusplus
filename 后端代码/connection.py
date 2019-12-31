# @Time    : 2019/12/23 10:49
# @Author  : Dreambee
# @File    : connection.py
# @Software: PyCharm
# @Desciption:
import cv2
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QImage
from flask import Flask, make_response, url_for, redirect, send_from_directory, send_file, request, render_template
from flask_cors import CORS
from flask_restful import Resource, Api
from flask_jsonpify import jsonify

from ResJson import ResJson
from check_face import store_face
from lib.InsightFace.face_verify import recognize
from lib.InsightFace.utils import prepare_facebank
from lib.cloud.ezapi import EZAPI


class Pictures(Resource):
    def __init__(self, device_no, mtcnn, targets, names, learner, conf):
        super(Pictures, self).__init__()
        self.device_no = device_no
        self.mtcnn = mtcnn
        self.targets = targets
        self.names = names
        self.learner = learner
        self.conf = conf

    def get(self):
        # 接受到请求后的响应函数
        # 向萤石云发送capture请求
        camera_api = EZAPI()
        camera_api.get_token()
        frame = camera_api.capture_picture(self.device_no)
        # 识别图像
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        try:
            img, res_names = recognize(img, self.mtcnn, self.targets, self.names, self.learner, self.conf)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            cv2.imwrite('templates/images/captured.png', img)
        except BaseException as err:
            # 有时候识别不到人脸
            print(err)
            result = {
                'status': 400,
                'msg': '检测不到人脸',
                'data': [], }
            response = make_response(jsonify(result))
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Origin'] = 'http://192.168.1.106:10000'
            response.headers['Access-Control-Allow-Methods'] = 'GET'
            response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
            return response
        result = {
            'status': 200,
            'msg': 'success',
            'data': {
               'names': res_names,
               'picture': 'http://192.168.1.107:9000/capturedimg',
            }, }
        response = make_response(jsonify(result))
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Origin'] = 'http://192.168.1.106:10000'
        response.headers['Access-Control-Allow-Methods'] = 'GET'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'

        return response


class ConThread(QThread):
    def __init__(self, device_no, mtcnn, targets, names, learner, conf):
        super(ConThread, self).__init__()
        self.app = Flask(__name__,  static_folder='C:/Users/21315/Desktop/Contest/Sin++/templates', static_url_path='')
        # CORS(self.app, resources=r'/*')
        self.api = Api(self.app)
        # 希望每次启动服务器都更新一下facebank
        _, _ = prepare_facebank(conf, learner.model, mtcnn, tta=False)
        args = {
            'device_no': device_no,
            'mtcnn': mtcnn,
            'targets': targets,
            'names': names,
            'learner': learner,
            'conf': conf,
        }
        self.api.add_resource(Pictures, '/capture', resource_class_kwargs=args)

        @self.app.route('/capturedimg')
        def img():
            # return send_file('templates/images/captured.png', mimetype='image/gif')
            return render_template('img.html')

        @self.app.route('/upload', methods=['GET', 'POST'])
        def upload_file():
            if request.method == 'POST':
                file = request.files['file']
                file.save('_faces/' + file.filename)
                image = cv2.imread('_faces/' + file.filename)
                student_no, student_name = file.filename.split('.')[0].split('_')
                if store_face(image, mtcnn, student_name):
                    # 如果成功检测到人脸，那么就更新facebank.pth和names.npy
                    _, _ = prepare_facebank(conf, learner.model, mtcnn, tta=False)
                    return ResJson("SUCCESS", "Upload Succeed.").to_json()
                else:
                    ResJson("FAILED", "Can't detect face. Please try again.").to_json()
            return ResJson("FAILED", "Please use POST instead of GET.").to_json()

    def run(self):
        self.app.run(
            host='10.214.149.20',
            port='9000')


if __name__ == '__main__':
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(Pictures, '/capture')
    app.run(
        host='192.168.1.107',
        port='9000')
