import time
import comtypes.client

#create object and connect
oag = comtypes.client.CreateObject("MaxIm.CCDCamera")
oag.LinkEnabled = True

#check link
if oag.LinkEnabled != True:
    print('Guider not connected, check if plugged in')
    oag.Quit()
    quit()

calibration = oag.GuiderCalState
if calibration != 0:
    if oag.GuiderRunning == False:
        print('unknown error raised')
    else:
        time.sleep(0.2) #delay between checks
        print('Guider currently calibrating')
else:
    print('Guider ready to calibrate')

#calibrate (or at least attempt to)
oag.GuiderCalibrate(3) # 3 second exposures

while oag.GuiderRunning == True:
    time.sleep(0.1)

calibrate_new = oag.GuiderCalState
if calibrate_new >= 1:
    print('No calibration procedure finished... wait')
    time.sleep(0.2)
else:
    if calibrate_new == 2:
        print('Calibration successful!')
    elif calibrate_new == 3:
        print('Calibration, failed')
    else:
        print('unknown error raised, quitting...')
        oag.Quit()
        quit()

print('Beginning shutdown procedure')
'shutdown procedure'
oag.Quit()