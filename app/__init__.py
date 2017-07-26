from sanic import Sanic

app = Sanic(__name__)

mysql_config = {
    'user': 'root',
    'password': '',
    'db': 'submit_info',
}

from app import views
