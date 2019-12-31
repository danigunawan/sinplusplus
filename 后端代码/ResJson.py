# @Time    : 2019/12/30 14:06
# @Author  : Dreambee
# @File    : ResJson.py
# @Software: PyCharm
# @Desciption: Response json的标准写法


class ResJson(object):
    def __init__(self, status, msg):
        super(ResJson, self).__init__()
        self.status = status
        self.msg = msg
        self.code = 200 if self.status == "SUCCESS" else 400
        self.data = []

    def to_json(self):
        res = {
            'code': self.code,
            'status': self.status,
            'msg': self.msg,
            'data': self.data,
        }
        return res
