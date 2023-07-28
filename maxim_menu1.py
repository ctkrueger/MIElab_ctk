#this is the menu of scriptable operations within the maxim application object
#most refer to guider because that is the device we will be using maxim for
#this file can be imported into another python executable file
#like it is in observe_baymax
import comtypes.client
import time

# creates the MaxIm.CCDCamera object
def guider_connect():
    object = comtypes.client.CreateObject("MaxIm.CCDCamera")
    time.sleep(.5) #extra time to be safe
    object.LinkEnabled = True
    time.sleep(.5) #rohan's magical fix to making GuiderExpose work
    #check link
    if object.LinkEnabled != True:
        print('Guider not connected, check if plugged in')
        object.Quit()
        return
    else:
        print('Guider connected')
    return object # has to return it so that it can be used by other commands

# disconnects the MaxIm.CCDCamera object, will be renamed with implementation of Cam1 
def guider_disconnect():
    object.Quit()
    print("Guider disconnected")
    return # does not return an object because its been disconnected

# just checks calcode, to be used on first startup only
def guider_calstate():
    #check link
    if object.LinkEnabled != True:
        print('Guider not connected, check if plugged in')
        object.Quit()
        return
    else:
        calcode = object.GuiderCalState
        print(f'Guider calibration code: {calcode}')
    return

#calibrates the guider by checking the calcode and then activating calibration
def guider_calibrate(duration):
    #check link
    if object.LinkEnabled != True:
        print('Guider not connected, check if plugged in')
        object.Quit()
        return
    else:
        pass
    #check calcode
    calcode = object.GuiderCalState
    match calcode: # checking that calcode is appropriate, could be clunky / unnecesary
        case 0: # needs calibration
            print(f'Guider preparing to calibrate: {duration}s exposures')
            object.GuiderCalibrate(duration)
            while object.GuiderMoving == True or object.GuiderRunning == True:
                time.sleep(1)
                continue
            time.sleep(5)
            calcode_new = object.GuiderCalState
            match calcode_new:
                case 2:
                    print('Guider Calibrated Successfully')
                    return
                case 3:
                    print('Guider calibration failed')
                    return
                case _:
                    print('Unknown error raised')
                    return
        case 1: # is calibrating, dont know why this would be raised
            print('Guider currently calibrating')
            while object.GuiderMoving == True or object.GuiderRunning == True:
                time.sleep(1)
                continue
            time.sleep(5)
            calcode_new = object.GuiderCalState
            match calcode_new:
                case 2:
                    print('Guider Calibrated Successfully')
                    return
                case 3:
                    print('Guider calibration failed')
                    return
                case _:
                    print('Unknown error raised')
                    return
        case 2: # already calibrated
            print('Guider Calibrated Successfully')
            return
        case 3: #tried to and failed
                    print('Guider calibration failed')
                    return
        case _: # no code that can be interpreted, just a precaution
            print('Unknown error raised')
            return

# take autoguider exposure, this is what locates guide stars
def guider_expose(duration, object, auto_select = True):
    #check link
    if object.LinkEnabled != True:
        print('Guider not connected, check if plugged in')
        object.Quit()
        return
    else:
        pass
    #check moving
    while object.GuiderMoving == True or object.GuiderRunning == True:
        time.sleep(1)
        continue
    time.sleep(.5) # rohan's magical fix to make GuiderExpose work

    # will pick the brightest star in the sky, will normally be true
    if auto_select == False:
        object.AutoSelectStar = False
    else:
        pass
    
    print(f'Guider connected, exposing for {duration}s')
    object.GuiderExpose(duration)
    while object.GuiderMoving == True or object.GuiderRunning == True:
        time.sleep(1)
        continue
    time.sleep(.5)

    #also will print the chosen guide star (if one is found)
    #when the coords are (0.0,0.0) you can assume that no star was found
    if auto_select == True:
        print('Checking for guide star...')
        x = object.GuiderXStarPosition # x position in image
        y = object.GuiderYStarPosition # y position in image
        time.sleep(0.5)
        print(f'Guide star coords: ({x},{y})')
        return
    else:
        return

#just prints the guidestar coords in case one is curious
def guidestar_coords():
    #check link
    if object.LinkEnabled != True:
        print('Guider not connected, check if plugged in')
        object.Quit()
        return
    else:
        pass
    #check moving
    while object.GuiderMoving == True or object.GuiderRunning == True:
        time.sleep(1)
        continue
    time.sleep(0.5)
    x = object.GuiderXStarPosition # x position in image
    y = object.GuiderYStarPosition # y position in image
    time.sleep(0.5)
    print(f'Guide star coords: ({x},{y})')
    return


