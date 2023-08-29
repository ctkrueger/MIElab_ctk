import comtypes.client
import time

#create guider object and link connect
guider = comtypes.client.CreateObject("MaxIm.CCDCamera")
guider.LinkEnabled = True

#Check to make sure camera is connected
if guider.LinkEnabled == False:
    print('Guider Camera failed to connect, quitting...')
    quit()
elif guider.LinkEnabled == True:
    print('Guider Camera connected, calibrating...')
    pass
else:
    print("Unknown Error during link, quitting...")
    quit()

#Calibrate Guider before use
# I am dumb and this doesnt work, will need to be fixed
if guider.GuiderCalState == 0:
    guider.GuiderCalibrate(3)

    #make sure nothing happens until guider becomes idle
    if guider.GuiderRunning == False and guider.GuiderCalState == 2:
        print('Guider calibration successful... exposing')
        pass
    elif guider.GuiderRunning == False and guider.GuiderCalState == 3:
        print('Guider calibration failed... try adjusting position')
    elif guider.GuiderRunning == True and guider.GuiderCalState == 1:
        time.sleep(0.5)
    else:
        print('Unknown Error during calibration... quitting')
        quit()
else:
    pass

#exposing guider cam for 5 seconds, should auto find guide star
guider.GuiderAutoSelectStar = True
guider.GuiderExpose(5)

#wait until idle to see if guide star is actually found
while guider.GuiderRunning == True:
    time.sleep(0.5)

#this is jank i hope can be made better
if guider.GuiderXStarPosition == 0.0 and guider.GuiderYStarPosition == 0.0:
    print('No suitable guide star found... try adjusting position')
else:
    x = guider.GuiderXStarPosition; y = guider.GuiderYStarPosition
    print(f'Guide Star found at (x, y): ({x}, {y})! Ready for tracking...')

    #make sure aggressiveness is set to 0 because no mount yet
    guider.GuiderAggressiveness = 0

    #tracking with 0.5s exposures
    guider.GuiderTrack(0.5)

#just track for 5 seconds or something
print('Guider Tracking...')
counter = 0
error_data = []
while counter > 10:
    if guider.GuiderRunning == True:
        error_x = guider.GuiderXError
        error_y = guider.GuiderYError
        error = [error_x, error_y]
        error_data.append(error)

        time.sleep(0.5)
        counter += 1
    elif guider.GuiderRunning == False:
        print('Guider stopped tracking unexpectedly')
        counter += 10
    else:
        print('Unkown Error whilst tracking, quitting...')
        quit()

guider.GuiderStop()
print('Guider has stopped tracking, retrieving error data')

print(error_data)

#shutdown procedure
guider.Quit()
quit()





