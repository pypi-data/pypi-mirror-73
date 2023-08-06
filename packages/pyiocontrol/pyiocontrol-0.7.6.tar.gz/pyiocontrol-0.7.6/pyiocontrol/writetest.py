from time import sleep
import pyiocontrol

p = pyiocontrol.Panel("test2")

print(p.mySensor)

while True:
    status = p.localUpdated
    if status:
        print(p.mySensor)
        print(p.localUpdated)

    else:
        print(p.lastStatus)
    sleep(.1)
    p.mySensor += 0.1
