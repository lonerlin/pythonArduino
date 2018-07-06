import tablib
import device
from flask import make_response,send_file
import time
import os
def excelExport(sensorid, top):
    print(top)
    r=device.getValue(sensorid,top)
    if(len(r)>0):
        headers = ("ID","传感器ID","传感器值","写入时间")
        dataset=tablib.Dataset(*r,headers=headers)
        print('dataset',os.linesep,dataset,os.linesep)
        with open('excel.xls','wb') as f:
            f.write(dataset.xls)

        return send_file('excel.xls')
if __name__ == "__main__":
    excelExport(3, 1000)