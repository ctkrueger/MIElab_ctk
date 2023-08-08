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

#turns on the tracking mode of a guider system once a guidestar is found
def guider_track(object, duration): # duration of each exposure
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

#stops the guider from completing its current task
def guider_stop(object):
    #check link
    if object.LinkEnabled != True:
        print('Guider not connected, check if plugged in')
        object.Quit()
        return
    else:
        pass
    
    #check moving
    if object.GuiderMoving == True or object.GuiderRunning == True:
        print('Stopping guider exposure/tracking')
        object.GuiderStop()
        return object
    else:
        print('Guider idle, awaiting further commands')
        return object

#prints a code number for the main ccd camera status, decode table in scripting manual
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

#takes a camera 1 exposure, this will be an numbered CCD Image that can be analyzed / saved
def cam_expose(object, duration, save_exposure = True):
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

    # third parameter ensures it is a light exposure and not a dark field 
    object.Expose(duration, 1, 0)
    
    #save cpu while image is processed
    while object.ImageReady == False:
        time.sleep(1)
        continue

    if save_exposure == True:
        file_path = input('File path for storing recent exposure?:\n')
        object.SaveImage(file_path)
        print(f'Exposure complete, image file saved to {file_path}')
    else:
        print('Exposure complete, image file open to get statistics')
    return object

#turns on the cam cooler, will take input setpoint so you  can use it as a warmer
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

#checks the current cam temperature, will only print a reasonable result while cooler on
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

#new method to utilize the cooler to warm the camera by setting the setpoint higher
#this gradually reduces the power of the cooler rather than just shutting off
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

    #takes an input for setpoint
    print(f'Warming CCD Camera to {setpoint} degrees, do not disconnect')
    object.TemperatureSetpoint = setpoint
    # to prevent exponential decay of warming as it approaches
    while object.Temperature <= (object.TemperatureSetpoint - 1):
        time.sleep(5) # five seconds to reduce number of messages that print  
        print(f'Current CCD cam temp is {object.Temperature} degrees')
        continue

    print(f'Camera warmed to {object.temperature}, turning cooler off')
    object.CoolerOn = False

    return object

#deconvolution analysis of a maxim DL document object (fits image)
def deconvolve(image, gain, method = 'rl'): # normally using Richardson-Lucy deconvolution
    method_code = None
    if method == 'rl': # richardson-lucy, reduces chi-square
        method_code = 2
    elif method == 'me': # maximum entropy, doesnt use chi-square
        method_code = 1
    else:
        print("unknown deconvolution method, options are RL or ME")
        return image
    
    #initializing deconvolution method(Richardson-Lucy or Maximum Entropy)
    image.Deconvolve(method_code)
    print('checkpoint 1')
    time.sleep(0.5)

    #setting the gain of the ccd camera, the rest of the noise stats are drawn from image data
    image.SetNoise(gain)
    print('checkpoint 2')
    time.sleep(0.5)

    #setting psf to be drawn from the raw image data, not fit to a gaussian or exponential
    image.SetPSF(2)
    print('Checkpoint 3')
    time.sleep(0.5)

    #starting the deconvolution iterations 
    image.Deconvolve(0)
    while image.IterationComplete == False:
        time.sleep(2)
        continue
    print('Initial Iterations Complete')
    chi_sqr = image.ChiSquare
    print(f'Chi Square value: {chi_sqr}')

    #query abt continuing iterations
    cont_q = input('Continue Iterating?(y/n):')
    match cont_q:
        case 'y': 
            image.Deconvolve(0)
            while image.IterationComplete == False:
                time.sleep(2)
                continue
            print('Secondary Iterations Complete')
            chi_new = image.ChiSquare
            print(f'New Chi Square value: {chi_new}')
        case 'n':
            image.Deconvolve(99)
    #saving the new image will have to be a new menu item
    return image

#saves image file in a specific local directory
def save_img(image, file_name):
    #folder where the images will be stored
    path_str = r'c:\Users\NUC\OneDrive\Documents\SavedFITS'
    #name of the image file, will only allow .fits and .fit because necessity only
    file_name = str(file_name)

    if file_name[-3:] == 'fit' or file_name[-4:] == 'fits':
        file_path = path_str + file_name
        image.SaveFile(file_path, 3, False, 1) #autostretch = false, FormatType = 1 (from web)
        time.sleep(0.5) #just to make sure everything has time to execute
        # image.Close() apparently the image.SaveFile() method closes the document
    else: #check condition to make sure it can be saved
        print('incorrect file type, should end with .fits or .fit')
    return

#opens file from a provided directory path, remember it has to be fits or fit
def open_file(file_path):
    #make sure string
    file_path = str(file_path)

    #make sure its a file that can be opened
    #again will only be .fit and .fits for necessity purposes
    if file_path[-3:] != 'fit' and file_path[-4:] != 'fits':
        print('Incorrect file path, needs to be a fits file from a known directory')
        return
    else:
        pass
    image = comtypes.client.CreateObject("MaxIm.Document")
    image.OpenFile(file_path)

    return image

