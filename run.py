from sanic import Sanic
from app import app

allow_host=""


db_settings = {
    'DB_HOST': 'localhost',
    'DB_NAME': 'appdb',
    'DB_USER': 'appuser'
}

app.config.update(db_settings) 
app.run(host="0.0.0.0",port=8000,workers=8)


