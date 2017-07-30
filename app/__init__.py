# -*- coding:utf-8 -*-
from sanic import Sanic
from sanic_jinja2 import SanicJinja2
from app import views

app = Sanic(__name__)

jinja = SanicJinja2(app, pkg_name='app')
