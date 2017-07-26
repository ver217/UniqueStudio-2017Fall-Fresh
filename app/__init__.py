#-*- coding:utf-8 -*-
from sanic import Sanic

app = Sanic(__name__)

mysql_config = {
    'user': 'root',
    'password': 'yyw19980424',
    'db': 'submit_info',
}

from app import views
