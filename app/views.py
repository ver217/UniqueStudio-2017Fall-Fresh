# -*- coding:utf-8 -*-
from app import data, app, mysql_config
from sanic.response import json
from sanic.exceptions import SanicException, ServerError
import pymysql


def db_setup():
    try:
        connection= pymysql.connect(host='localhost',
                             user=mysql_config['user'],
                             password=mysql_config['password'],
                             db=mysql_config['db'],
                             charset='utf8mb4')
        return connection
    except Exception:
        raise ServerError("Can't connect to MySQL Server!", status_code=500)


def error_code(code):
    return json({"status": "fail", "error_code": code})


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
    info=request.json
    code = data.submit(info)
    if code:
        result["status"] = "fail"
        result["error_code"] = code
    return json(result)


@app.route("/api/signup/post", methods=["POST"])
async def post(request):
    result = {
        "status": "success"
    }
    try:
        resume,name=request.files.get('resume'), request.form['name'][0]
        ext = resume.name.split('.')[-1]
        code = data.save_resume(name, ext, resume.body)
        if code:
            result["status"] = "fail"
            result["error_code"] = code
        return json(result)
    except Exception:
        return error_code(713)


@app.route("/api/signup/getinfo", methods=["GET"])
async def get_info(request):
    result = data.get_info()
    return json({"list": result})


@app.route("/api/signup/getresume", methods=["POST"])
async def get_resume(request):
    try:
        name=request.json['name']
        result = data.get_resume(name)
        if type(result) == int:
            return error_code(result)
        else:
            return json({"result": result})
    except Exception as e:
        print(e)
        return error_code(713)


@app.exception(SanicException)
def error(request, exception):
    return error_code(710)
