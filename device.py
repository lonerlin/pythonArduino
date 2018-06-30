import db
import datetime

DBPath = 'webDB.db'


def updateDevice(userid, deviceid, sensorid, state=0, value=0):
    if (len(findSensor(userid, deviceid, sensorid)) > 0):
        
        sql_update =''' UPDATE devices SET state = ?, value=? 
                  WHERE (userID=? and deviceID=? and sensorID=?)  '''
        db.update(db.get_conn(DBPath), sql_update, [(state, value, userid, deviceid, sensorid)])
    else:
        sql_insert = ''' insert into devices (userID, deviceID, sensorID, state, value) 
            VALUES (?,?,?,?,?);
            '''
        db.save(db.get_conn(DBPath), sql_insert, [(userid, deviceid, sensorid, state, value)])


def findSensor(userid, deviceid, sensorid):
    sql_select = '''Select state,value from devices 
                  where  userID=? and  deviceID=? and sensorID=?'''
    r = db.fetchone(db.get_conn(DBPath), '''Select state from devices where deviceID=? and userID=? and sensorID=?''',
                    (userid, deviceid, sensorid))
    return r


def findState(userid, deviceid, sensorid):
    r = findSensor(userid, deviceid, sensorid)
    if (len(r) > 0):
        return r[0][0]
    else:
        return None


def findValue(userid, deviceid, sensorid):
    r = findSensor(userid, deviceid, sensorid)
    if (len(r) > 0):
        return r[0][1]
    else:
        return None


def addValue(sensorid, value):
    sql_select = ''' insert into readyOnlyData (sensorID, value,updateTime)  
                  values(?,?,?) 
              '''
    db.save(db.get_conn(DBPath), sql_select, [(sensorid, value, datetime.datetime.now())])


def getValue(sensorid):
    sql_select = '''select * from readyOnlyData
            where SensorID=? order by id desc 
            Limit 20 
            '''
    return db.fetchone(db.get_conn(DBPath), sql_select, [sensorid])




def testUpdate():
    updateDevice(1,1,1,1,234)
def testAddReadOnlyData():
    addValue(1,41)
def main():
    testAddReadOnlyData()


if __name__ == '__main__':
    main()
