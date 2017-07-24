from sanic import sanic
from sanic.response import json

app = Sanic()

@app.route("/api/signup/submit")
async def submit(request):
    return json({"hello":"world"})

if __name__=="__main__":
    app.run(host="0.0.0.0",port=8000)