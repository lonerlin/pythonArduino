from simpletcp.tcpserver import TCPServer
import queue
from urllib import parse
import device

def echo(ip,queue,data):

    redata=(analyzeData(data)+'\r\n').encode('utf-8')

    queue.put(redata)


def analyzeData(data):
    cmd=parse.parse_qs(data.decode('utf-8').strip())
    print (cmd)
    command = cmd['cmd'][0]
    sensorid=int(cmd['sensorid'][0])
    value = 0
    deviceid = 1
    userid = 1
    state = -1
    if 'value' in cmd.keys():
        value=int(cmd['value'][0])
    if 'userid' in cmd.keys():
        userid=int(cmd['userid'][0])
    if 'deviceid' in cmd.keys():
        deviceid=int(cmd['deviceid'][0])
    if 'state' in cmd.keys():
        state=int(cmd['state'][0])
    if (command == 'publish'):
       return getState(userid, deviceid, sensorid)
    elif (command == 'upload'):
        setReadOnleValue(sensorid, value)
        return "cmd=upload&res=1"
    elif (command == 'subscribe'):
        return "cmd=subscribe&res=1"
    return ""

def getState(userid, deviceid, sensorid):
    return "cmd=publish&sensorid=%d&state=%d" % (sensorid, device.findState(userid, deviceid, sensorid))

def setReadOnleValue(sensorid,value):
    device.addValue(sensorid,value)


server = TCPServer("0.0.0.0", 5000, echo)
server.run()