# -*- coding:utf-8 -*-
import asyncio_redis
from app import data, app, jinja, monkey_patch
from sanic.response import json, redirect
from sanic_session import RedisSessionInterface
from typing import Callable

admin = {
    'id': 'uniquestudio',
    'password': 'P@ssw0rd'
}


class Redis:
    _pool = None

    async def get_redis_pool(self):
        if not self._pool:
            self._pool = await asyncio_redis.Pool.create(
                host='localhost', port=6379, poolsize=10
            )
        return self._pool


def new_init(
        self, redis_getter: Callable,
        domain: str = None, expiry: int = 600,
        httponly: bool = True, cookie_name: str = 'session',
        prefix: str = 'session:'):
    self.redis_getter = redis_getter
    self.expiry = expiry
    self.prefix = prefix
    self.cookie_name = cookie_name
    self.domain = domain
    self.httponly = httponly


class NewRedisSessionInterface(RedisSessionInterface):
    pass


NewRedisSessionInterface.__init__ = new_init

redis = Redis()

session_interface = NewRedisSessionInterface(redis.get_redis_pool)


@app.middleware('request')
async def add_session_to_request(request):
    await session_interface.open(request)


@app.middleware('response')
async def save_session(request, response):
    await session_interface.save(request, response)


def error_code(code):
    return json({"status": "fail", "error_code": code})


@app.listener('before_server_start')
async def setup_static(app, loop):
    app.static(app, '/static', './app/static')
    app.static = monkey_patch.static
    app.static(app, '/api/signup/resume', './resume')


@app.listener('after_server_start')
async def notify_server_started(app, loop):
    print('Server successfully started! 0w0')


@app.listener('before_server_stop')
async def notify_server_stopping(app, loop):
    print('Server shutting down... 0w0')


@app.route("/system/login", methods=["GET"])
async def login_html(request):
    if 'Auth' not in request['session']:
        request['session']['Auth'] = 0
    elif request['session']['Auth'] == 1:
        return redirect(app.url_for('info_list'))
    return jinja.render('login.html', request, title='Login')


@app.route("/system/login/post", methods=["POST"])
async def login_post(request):
    if request.form['id'][0] == admin['id'] and request.form['pw'][0] == admin['password']:
        request['session']['Auth'] = 1
        return redirect(app.url_for('info_list'))
    else:
        return redirect(app.url_for('login_html'))


@app.route("/system/list", methods=["GET"])
async def info_list(request):
    if 'Auth' not in request['session']:
        request['session']['Auth'] = 0
    elif request['session']['Auth'] == 1:
        result = data.get_info()
        return jinja.render('list.html', request, info=result, title='List')
    return redirect(app.url_for('login_html'))


@app.route("/api/signup/submit", methods=["POST"])
async def submit(request):
    result = {
        "status": "success"
    }
    info = request.json
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
        resume, name = request.files.get('resume'), request.form['name'][0]
        ext = resume.name.split('.')[-1]
        code = data.save_resume(name, ext, resume.body)
        if code:
            result["status"] = "fail"
            result["error_code"] = code
        return json(result)
    except ValueError:
        return error_code(713)


@app.route("/api/signup/getinfo", methods=["GET"])
async def get_info(request):
    result = data.get_info()
    return json({"list": result})


@app.route("/api/signup/getresume", methods=["POST"])
async def get_resume(request):
    try:
        name = request.json['name']
        result = data.get_resume(name)
        if type(result) == int:
            return error_code(result)
        else:
            return json({"result": result})
    except Exception as e:
        print(e)
        return error_code(713)

# @app.exception(SanicException)
# def error(request, exception):
#    return error_code(710)
