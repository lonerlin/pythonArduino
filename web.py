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

   pass



if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5001,debug=True)