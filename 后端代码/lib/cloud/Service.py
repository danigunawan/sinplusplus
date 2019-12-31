from flask import (Flask, render_template, request,
                    jsonify, url_for, send_from_directory,
                   current_app, send_file)
from werkzeug.utils import secure_filename
import os
from lib.cloud.log import MyLog
app = Flask(__name__, template_folder="html", static_folder="upload")
app.config['UPLOAD_FOLDER'] = 'upload'
mylog = MyLog()

# 显示原图和上一次图片
@app.route('/')
def index():
    return render_template("index.html")


@app.route('/hello')
def hello():
    return 'Hello, Flask'


@app.route('/user/<username>')
def user(username):
    return render_template("hello.html", name=username)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'do login business'
    else:
        return 'show login form'


@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    # mylog.info("just visited!")
    if request.method == 'POST':
        # mylog.info(request.files)
        file = request.files['file']
        file.save('upload/'+secure_filename(file.filename))
        return "OK"
    else:
        return render_template('upload.html')


@app.route('/download_file')
def download_file():
    return render_template('download.html')

# 可行
@app.route('/upload/<filename>')
def upload(filename=None):
    uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, filename=filename)

# 有问题
@app.route('/download/<filename>')
def download(filename):
    path = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'], filename)
    print(path)
    return app.send_static_file(path)

# json format
@app.route('/me')
def me_api():
    user = {'username':'hujun', 'theme':'black'}
    return {
        "username": user.username,
        "theme": user.theme,
    }


@app.route("/users")
def users_api():
    users = {'username':'hujun', 'theme':'black'}
    return jsonify([user.to_json() for user in users])


@app.route("/token")
def token():
    request.path=""
    request.method = 'POST'
    return request.get_json()


@app.route("/student")
def student():
    name = request.args.get('name')
    id = request.args.get('id')
    mylog.info("{0}, {1}".format(name, id))
    return "OK"


if __name__ == '__main__':
    print("service start run")
    app.run(host="0.0.0.0", port=9099)