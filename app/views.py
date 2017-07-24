from app import data
from sanic.response import json

@app.listener('before_server_start')
async def setup_db(app, loop):
    app.db = await db_setup()

@app.listener('after_server_start')
async def notify_server_started(app, loop):
    print('Server successfully started! 0w0')

@app.listener('before_server_stop')
async def notify_server_stopping(app, loop):
    print('Server shutting down... 0w0')

@app.listener('after_server_stop')
async def close_db(app, loop):
    await app.db.close()

@app.route("/api/signup/submit",methods=["POST"])#,host=allow_host)
async def submit(request):
    result={
        "status": "success"
    }
    info=request.json
    resume=request.files.get('resume')
    code=data.submit(info,resume)
    if code!=0:
        result["status"]="fail"
        result["error_code"]=code
    return json(result)

@app.middleware('request')
async def print_on_request(request):
    name=request.json['name']
    group = request.json['group']
    print("Received %s - %s" %(group,name))

@app.middleware('response')
async def print_on_response(request, response):
    print("%s : %s"%(response.json['status'],response.json['error_code']))
    print()