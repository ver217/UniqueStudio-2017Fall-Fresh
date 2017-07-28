# -*- coding:utf-8 -*-
from sanic import Sanic
from sanic_jinja2 import SanicJinja2

app = Sanic(__name__)

jinja = SanicJinja2(app,pkg_name='app')

mysql_config = {
    'user': 'root',
    'password': 'yyw19980424',
    'db': 'submit_info',
}

from app import views
