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
def guider_disconnect(object):
    object.Quit()
    print("Guider disconnected")
    return # does not return an object because its been disconnected

# just checks calcode, to be used on first startup only
def guider_calstate(object):
    #check link
    if object.LinkEnabled != True:
        print('Guider not connected, check if plugged in')
        object.Quit()
        return
    else:
        calcode = object.GuiderCalState
        print(f'Guider calibration code: {calcode}')
    return object

#calibrates the guider by checking the calcode and then activating calibration
def guider_calibrate(object, duration):
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
                    return object
                case 3:
                    print('Guider calibration failed')
                    return object
                case _:
                    print('Unknown error raised')
                    return object
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
                    return object
                case 3:
                    print('Guider calibration failed')
                    return object
                case _:
                    print('Unknown error raised')
                    return object
        case 2: # already calibrated
            print('Guider Calibrated Successfully')
            return object
        case 3: #tried to and failed
                    print('Guider calibration failed')
                    return object
        case _: # no code that can be interpreted, just a precaution
            print('Unknown error raised')
            return object

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
        return object
    else:
        return object

#just prints the guidestar coords in case one is curious
def guidestar_coords(object):
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
    return object

def guider_track(object, duration):
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
    
    x = object.GuiderXStarPosition # x position in image
    y = object.GuiderYStarPosition # y position in image
    print('Beginning guidestar tracking')
    print(f'Guidestar coords: ({x}, {y})')

    object.GuiderTrack(duration)
    #check moving
    return object

def guider_stop(object):
    #check link
    if object.LinkEnabled != True:
        print('Guider not connected, check if plugged in')
        object.Quit()
        return
    else:
        pass
    
    if object.GuiderMoving == True or object.GuiderRunning == True:
        print('Stopping guider exposure/tracking')
        object.GuiderStop()
        return object
    else:
        print('Guider idle, awaiting further commands')
        return object

def cam_status(object):
    #check link
    if object.LinkEnabled != True:
        print('Guider not connected, check if plugged in')
        object.Quit()
        return
    else:
        pass
    #check guider moving
    while object.GuiderMoving == True or object.GuiderRunning == True:
        time.sleep(1)
        continue

    #check camera 1 status if it applies to the situation
    status = object.CameraStatus
    print(f'Camera 1 Status Code: {status}')
    return object


def cam_expose(object, duration):
    #check link
    if object.LinkEnabled != True:
        print('Guider not connected, check if plugged in')
        object.Quit()
        return
    else:
        pass
    #check guider moving
    while object.GuiderMoving == True or object.GuiderRunning == True:
        time.sleep(1)
        continue

    object.Expose(duration, 1, 0)
    
    while object.ImageReady == False:
        time.sleep(1)
        continue

    image = comtypes.client.CreateObject("MaxIm.Document")
    #object.SaveImage('Enter file path for images here, ending with image.fit')
    print('Exposure complete, image file open to get statistics')
    return image, object

def cam_cooler(object):
    #check link
    if object.LinkEnabled != True:
        print('Guider not connected, check if plugged in')
        object.Quit()
        return
    else:
        pass
    #check guider moving
    while object.GuiderMoving == True or object.GuiderRunning == True:
        time.sleep(1)
        continue
    #default setpoint
    object.TemperatureSetpoint = -20
    object.CoolerOn = True
    time.sleep(0.5) # this might work like rohan's trick for quiderexpose
    print(f'Cooling CCD camera to -20 degrees')
    time.sleep(0.5) # just to be safe
    print(f'Current CCD cam temp is {object.Temperature} degrees')
    
    return object

def cam_temp(object):
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

    current_temp = object.Temperature
    print(f'Current CCD cam temp is {current_temp} degrees')
    return object

def warm(object, setpoint):
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

    print(f'Warming CCD Camera to {setpoint} degrees, do not disconnect')
    object.TemperatureSetpoint = setpoint
    while object.Temperature <= (object.TemperatureSetpoint - 1): # to prevent exponential decay of warming as it approaches
        time.sleep(2)  
        print(f'Current CCD cam temp is {object.Temperature} degrees')
        continue

    print(f'Camera warmed to {object.temperature}, turning cooler off')
    object.CoolerOn = False

    return object

def deconvolve(object, image):
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
    image.Deconvolve(2)
    print('checkpoint 1')
    time.sleep(0.5)
    image.SetPSF(2)
    print('checkpoint 2')
    time.sleep(0.5)
    image.Deconvolve(0)
    while image.IterationComplete == False:
        time.sleep(2)
        continue
    print('Checkpoint 3')
    image.Deconvolve(99)
    return image, object





    


