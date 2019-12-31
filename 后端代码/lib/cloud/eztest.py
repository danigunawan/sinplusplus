"""
@time:      2019-12-09 10:03:06
@version:   v1.0
@author：   hujunchina@outlook.com
"""
import requests
from datetime import datetime
import os

def get_token():
    appKey = "c127ab47d5dc450088b7c9ce8a8aac85"
    appSecret = "9316c6d3ece1d67e7eb8b386fb365fb5"
    querystring = {"appKey": appKey,"appSecret": appSecret}
    url = "https://open.ys7.com/api/lapp/token/get"
    req = requests.request("POST", url, params=querystring)
    return req.json()

def send_pic():
    start_time = datetime.now().strftime("%H:%M:%S")
    url = ''
    end_time = datetime.now().strftime("%H:%M:%S")

def get_pic():
    start_time = datetime.now().strftime("%H:%M:%S")
    url = 'https://s2.ax1x.com/2019/12/09/QdLwUP.jpg'
    r = requests.get(url, stream=True)
    if r.status_code is 200:
        with open("img/new.jpg", 'wb') as f:
            for chunk in r:
                f.write(chunk)
    end_time = datetime.now().strftime("%H:%M:%S")
    print("{0}, {1}".format(start_time, end_time))


def file_name():
    l = len(os.listdir("img"))
    pic = "{0}.jpg".format(l+1)
    path = os.path.join("img", pic)
    return path

if __name__ == '__main__':
    # raw_json = get_token()
    # print(raw_json)
    # print(raw_json['data']['accessToken'])
    # get_pic()
    print(file_name())
