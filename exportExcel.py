import tablib
import device
import time
import os
def excelExport(sensorid,top=20):
    r=device.getValue(sensorid,top)
    if(len(r)>0):
        headers = ("ID","传感器ID","传感器值","写入时间")
        dataset=tablib.Dataset(*r,headers=headers)
        print('dataset',os.linesep,dataset,os.linesep)

if __name__ == "__main__":
    excelExport(3, 1000)