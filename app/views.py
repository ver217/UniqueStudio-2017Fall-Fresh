# -*- coding:utf-8 -*-
from app import data, app, mysql_config
from sanic.response import json
from sanic.exceptions import INTERNAL_SERVER_ERROR_HTML
import pymysql


def db_setup():
    connection = pymysql.connect(host='localhost',
                                 user=mysql_config['user'],
                                 password=mysql_config['password'],
                                 db=mysql_config['db'],
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection


@app.listener('before_server_start')
async def setup_db(app, loop):
    app.db = db_setup()
    app.static('/api/signup/resume', './resume')


@app.listener('after_server_start')
async def notify_server_started(app, loop):
    print('Server successfully started! 0w0')


@app.listener('before_server_stop')
async def notify_server_stopping(app, loop):
    print('Server shutting down... 0w0')


@app.listener('after_server_stop')
async def close_db(app, loop):
    app.db.close()


@app.route("/api/signup/submit", methods=["POST"])
async def submit(request):
    result = {
        "status": "success"
    }
    info = request.json
    code = data.submit(info)
    if code != 0:
        result["status"] = "fail"
        result["error_code"] = code
    return json(result)


@app.route("/api/signup/post", methods=["POST"])
async def post(request):
    result = {
        "status": "success"
    }
    resume = request.files.get('resume').body
    ext = request.files.get('resume').name.split('.')[-1]
    name = request.form['name'][0]
    code = data.save_resume(name, ext, resume)
    if code != 0:
        result["status"] = "fail"
        result["error_code"] = code
    return json(result)


@app.route("/api/signup/getinfo", methods=["GET"])
async def get_info(request):
    result = data.get_info()
    return json({"list": result})


@app.route("/api/signup/getresume", methods=["POST"])
async def get_resume(request):
    name = request.json['name']
    result = data.get_resume(name)
    if result == -1:
        return 715
    elif result == -2:
        return 716
    elif result != None:
        return json({"result": result})


@app.exception(INTERNAL_SERVER_ERROR_HTML)
def error(request, exception):
    return json({"status": "fail", "error_code": 710})
