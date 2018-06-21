import db
DBPath='webDB.db'
def updateDevice(userid,deviceid,sensorid,state=0,value=0):
    if (len(findSensor(userid,deviceid,sensorid))>0):
        sql_update=' UPDATE devices SET state = ?,value=? ' \
               'WHERE (userID=? and deviceID=? and sensorID=?) '
        db.update(db.get_conn(DBPath),sql_update,[(state,value,userid,deviceid,sensorid)])
    else:
        sql_insert=''' insert into devices (userID, deviceID, sensorID, state, value) 
            VALUES (1,1,1,0,0);
            '''
        db.save(db.get_conn(DBPath),sql_insert,[(userid,deviceid,sensorid,state,value)])

def findSensor(userid,deviceid,sensorid):
    sql_select='''Select state,value from devices 
                  where  userID=? and  deviceID=? and sensorID=?'''
    r = db.fetchone(db.get_conn(DBPath), '''Select state from devices where deviceID=? and userID=? and sensorID=?''',(userid, deviceid, sensorid))
    return r
def findState(userid,deviceid,sensorid):
    r = findSensor(userid,deviceid,sensorid)
    if (len(r)>0):
        return r[0][0]
    else:
        return None


def findValue(userid, deviceid, sensorid):
    r = findSensor(userid, deviceid, sensorid)
    if (len(r) > 0):
        return r[0][1]
    else:
        return None