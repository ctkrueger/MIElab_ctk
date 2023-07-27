import comtypes.client
import time

def guider_connect():
    object = comtypes.client.CreateObject("MaxIm.CCDCamera")
    time.sleep(.5)
    object.LinkEnabled = True
    time.sleep(.5)
    #check link
    if object.LinkEnabled != True:
        print('Guider not connected, check if plugged in')
        object.Quit()
        return
    else:
        print('Guider connected')
    return object

def guider_disconnect():
    object.Quit()
    print("Guider disconnected")
    return

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
    match calcode:
        case 0:
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
        case 1:
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
        case 2:
            print('Guider Calibrated Successfully')
            return
        case 3:
                    print('Guider calibration failed')
                    return
        case _:
            print('Unknown error raised')
            return

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

    if auto_select == True:
        print('Checking for guide star...')
        x = object.GuiderXStarPosition
        y = object.GuiderYStarPosition
        time.sleep(0.5)
        print(f'Guide star coords: ({x},{y})')
        return
    else:
        return

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
    x = object.GuiderXStarPosition
    y = object.GuiderYStarPosition
    time.sleep(0.5)
    print(f'Guide star coords: ({x},{y})')
    return


