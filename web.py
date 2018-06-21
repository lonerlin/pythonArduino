from flask import Flask, render_template, request, redirect, url_for
import db
import device

app = Flask(__name__)
#app.config['DEBUG'] = True
dbPath='webDB.db'


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
def getstate():
    deviceid=request.args.get("deviceid",0)
    userid=request.args.get("userid",0)
    sensorid=request.args.get("sensorid",0)
    print( str(deviceid) + ' '+str(userid) + ' '+ str(sensorid))
    return "state:" + str(device.findState(userid,deviceid,sensorid))

if __name__ == "__main__":
	app.run(host='0.0.0.0',debug=True)