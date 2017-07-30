# -*- coding:utf-8 -*-
import sanic
from sanic import Sanic
from app import monkey_patch

sanic.static.register = monkey_patch.register
from app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, workers=4)
