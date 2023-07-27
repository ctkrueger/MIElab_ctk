import time
import comtypes.client
import subprocess

#create com object and connect
oag = comtypes.client.CreateObject("MaxIm.CCDCamera")
oag.LinkEnabled = True

#check link is enabled
if oag.LinkEnabled == True:
    print('Guider Connected, ready to expose')
elif oag.LinkEnabled == False:
    print('Guider failed to connect, check that its plugged in')
else:
    print('unknown error raised, quitting...')
    quit()

time.sleep(0.5) #rohan's magical fix to make GuiderExpose work
#exposing the guider for 3 seconds
oag.GuiderExpose(5)

#wait for the exposure to finish
while oag.GuiderRunning == True:
    time.sleep(0.1) #supposedly saves cpu usage

print('Exposure completed, shutting down')

# Shutdown procedure
oag.Quit()