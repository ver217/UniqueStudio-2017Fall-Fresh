#-*- coding:utf-8 -*-
from sanic import Sanic
from app import app

allow_host = ""

app.run(host="0.0.0.0", port=8000, workers=8)
