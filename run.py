from sanic import Sanic
from app import views

allow_host=""

app = Sanic()

db_settings = {
    'DB_HOST': 'localhost',
    'DB_NAME': 'appdb',
    'DB_USER': 'appuser'
}

app.config.update(db_settings)

if __name__=="__main__":
    app.run(host="0.0.0.0",port=8000,workers=8)
