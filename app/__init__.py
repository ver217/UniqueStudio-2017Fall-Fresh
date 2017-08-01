# -*- coding:utf-8 -*-
from sanic import Sanic
from sanic_jinja2 import SanicJinja2
from sanic_cors import CORS,cross_origin

app = Sanic(__name__)
CORS(app)

jinja = SanicJinja2(app, pkg_name='app')
from app import views,data
