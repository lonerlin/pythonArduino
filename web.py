from flask import Flask, render_template, request, redirect, url_for,session
import db
import device
import time
from gpcharts import figure

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
#app.config['DEBUG'] = True
dbPath='webDB.db'

@app.route('/table/<int:sensorid>', methods = ['POST', 'GET'])

def buildTable(sensorid):
    r = device.getValue(sensorid)
    print(len(r))
    if (len(r) > 0):
        return render_template('table.html', table=r)
    return None

@app.route('/chart/<int:sensorid>', methods = ['POST', 'GET'])

def buildChart(sensorid):
    r=device.getValue(sensorid)
    if(len(r)>0):
        fig3 = figure()
        fig3.title = 'Weather over Days'
        fig3.ylabel = 'Temperature'
        fig3.height = 800
        fig3.width = 1200
        xVals=['时间']
        yVals=['温度']
        for value in r:
            xVals.append(value[3][11:19])
            yVals.append(value[2])
        fig3.plot(xVals,yVals)
    return None

@app.route('/control/', methods = ['POST', 'GET'])

def index():
        state1=0
        state2=0
        r=device.findSensor(1,1,1)
        if(len(r)>0):
            state1=r[0][0]
        r=device.findSensor(1,1,2)
        if(len(r)>0):
            state2=r[0][0]
        return render_template('index.html', state1=state1, state2=state2)


@app.route('/control/<int:sensorid>/<int:state>', methods = ['POST', 'GET'])
def ledSwitch(sensorid,state):
    print("Sensorid:",sensorid)
    print("state:",state)
    if (state == 1):
        state = 0
    else:
        state = 1
    device.updateDevice(1,1,sensorid,state)
    return  redirect('/control/')

@app.route('/')
def deviceroute():
    for x in request.headers:
        print(x)
    for x in request.args:
        print(x)
    for x in request.values:
        print(x)
    return None
    '''
    print(request.values)
    deviceid=request.args.get("deviceid",0)
    userid=request.args.get("userid",0)
    sensorid=request.args.get("sensorid",0)
    command=request.args.get("cmd","")
    value=request.args.get("value",0)
    state=request.args.get("state",-1)
    print( str(deviceid) + ' '+str(userid) + ' '+ str(sensorid))

    if (command=='publish'):
        getState(userid,device,sensorid)
    elif(command=='upload'):
        setReadOnleValue(sensorid,value)
        return "cmd=upload&res=1"
    elif(command=='subscribe'):
        session['userID']=userid
        return "cmd=subscribe&res=1"
    '''

def getState(userid, deviceid, sensorid):
    return "cmd=publish&sensorID=%d&state=%d" % (sensorid,device.findState(userid,deviceid,sensorid))


def setReadOnleValue(sensorid,value):
    device.addValue(sensorid,value)
    return "sensorid:"+ str(sensorid) + "write:ok;"
if __name__ == "__main__":
	app.run(host='0.0.0.0',debug=True)