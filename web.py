from flask import Flask, render_template, request, redirect, url_for,session
import db
import device
import time
from gpcharts import figure

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
#app.config['DEBUG'] = True
dbPath='webDB.db'

@app.route('/chart/<int:sensorid>', methods = ['POST', 'GET'])

def buildChart(sensorid):
    r=device.getValue(sensorid)
    if(len(r)>0):
        fig3 = figure()
        fig3.title = 'Weather over Days'
        fig3.ylabel = 'Temperature'
        # modify size of graph
        fig3.height = 800
        fig3.width = 1200
        xVals=['时间']
        yVals=['温度']
        for value in r:
            xVals.append(value[1][11:19])
            yVals.append(value[0])
        fig3.plot(xVals,yVals)
    return None
@app.route('/control/', methods = ['POST', 'GET'])

def index():
    if request.method == 'POST':
        values = request.form['submit']
        print(values[5:])
        if(values[5:]=='ON'):
            ledState='OFF'
            sColor='red'
            data = 1
        else:
            ledState='ON'
            sColor='black'
            data = 0
        print(data)
        device.updateDevice(1, 1, 1, data)
        return render_template('index.html', state=ledState,sColor=sColor)
    r=device.findSensor(1,1,1)
    if(r[0][0]):
        ledState='OFF'
        sColor='red'
    else:
        ledState='ON'
        sColor='black'
    return render_template('index.html', state=ledState, sColor=sColor)



@app.route('/', methods = ['POST', 'GET'])
def deviceroute():
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


def getState(userid, deviceid, sensorid):
    return "cmd=publish&sensorID=%d&state=%d" % (sensorid,device.findState(userid,deviceid,sensorid))


def setReadOnleValue(sensorid,value):
    device.addValue(sensorid,value)
    return "sensorid:"+ str(sensorid) + "write:ok;"
if __name__ == "__main__":
	app.run(host='0.0.0.0',debug=True)