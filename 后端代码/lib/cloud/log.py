"""
@time:      2019-12-09 10:03:06
@version:   v1.0
@author：   hujunchina@outlook.com
"""
import datetime


class Log(object):
    def __init__(self):
        print("{0}[INFO] Log service started".format(self.get_time()))

    def get_time(self):
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def info(self, msg=""):
        print("{0}[INFO] {1}".format(self.get_time(), msg))

    def error(self, msg=""):
        print("{0}[ERROR] {1}".format(self.get_time(), msg))

    def warning(self, msg=""):
        print("{0}[WARNING] {1}".format(self.get_time(), msg))


if __name__ == '__main__':
    log = Log()
    log.info('test')
    log.error('error')
    log.warning('warning')