import time
import comtypes.client

#create object and connect
oag = comtypes.client.CreateObject("MaxIm.CCDCamera")
oag.LinkEnabled = True

#checking link
if oag.LinkEnabled == True:
    print('Guider connected, looking for guide star')
elif oag.LinkEnabled == False:
    print('Guider not connected, check if plugged in')
    oag.Quit()
    quit()
else:
    print('unknown error raised, quitting...')
    oag.Quit()
    quit()

#make sure guide star initializes automatically
oag.GuiderAutoSelectStar = True
#exposing for 3 seconds
oag.GuiderExpose(3)

while oag.GuiderRunning == True:
    time.sleep(0.1) # cpu usage reduction 

#check if guide star was found
x = oag.GuiderXStarPosition
y = oag.GuiderYStarPosition

print(f'Guide star coords: ({x},{y})')

#shutdown procedure
oag.Quit()