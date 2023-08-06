from time import sleep
import pyiocontrol

p = pyiocontrol.Panel("test2")

print(p.mySensor)

while True:
    status = p.lastStatus
    #print(status)
    if status == 0:
        print(p.mySensor)
        print(status)

    else:
        print(p.lastStatus)
    sleep(.5)
    p.mySensor += 0.5
