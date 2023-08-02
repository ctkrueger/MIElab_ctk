#named after Baymax the personal healthcare companion from the 2014 film Big Hero 6
#the CLI in which commands to the two cameras will be sent
#to continue operating commands (including disconnect) reply to 'Operate Command?' with 'y'
#after disconnecting all cameras, then respond with 'n' to close the maxim dl app object

import comtypes.client
import maxim_menu1
import time
#all possible commands at this time
options = ['connect', 'disconnect', 'guiderexpose', 'calibrate', 'calstate',\
    'guidestar', 'track', 'guiderstop', 'status', 'camexpose', 'cooler', \
    'temp', 'warm', 'deconvolve', 'list']
#session = 1 means the session with the menu is open;
#when session = 0, the session closes and all of maxim dl will close
session = 1
object = None
image = None
while session == 1:
    command_bool = input('Operate Command? (y/n)') #will prompt about camera connection also
    match command_bool:
        case "y":
            app = comtypes.client.CreateObject("MaxIm.Application")
            command_string = input('Command?:\n') #must be typed lower case as one word
            match command_string:
                case "connect": #establishes a maxim.ccdcamera object
                    object = maxim_menu1.guider_connect()
                    session = 1
                    continue
                case "disconnect": #quits the camera object, unsure if quits both
                    maxim_menu1.guider_disconnect(object)
                    session = 1
                    continue
                case "guiderexpose": #takes a guider exposure, will change when add normal expose
                    duration = input('Duration in s?: ') #respond in float value
                    duration = float(duration)
                    maxim_menu1.guider_expose(duration, object)
                    session = 1
                    continue
                case "calibrate": #calibrates guider, dont think we'll have to add ccdcal
                    duration = input('Duration in s?: ') #respond in float value
                    duration = float(duration)
                    maxim_menu1.guider_calibrate(object, duration)
                    session = 1
                    continue
                case "calstate": #returns the calibration code of the guider
                    maxim_menu1.guider_calstate(object) # refer to manual for codes 
                    session = 1
                    continue
                case "guidestar": #returns coords of guide star in photo
                    maxim_menu1.guidestar_coords(object)
                    session = 1
                    continue
                case "track": #tracks the currently selected guidestar
                    duration = input('Duration in s?: ') # respond in float value
                    duration = float(duration)
                    maxim_menu1.guider_track(object, duration)
                    session = 1
                    continue
                case "guiderstop": #stops guider tracking, returns cam to idle
                    maxim_menu1.guider_stop(object)
                    session = 1
                    continue
                case "status": #checks status of camera1, the ccd camera
                    maxim_menu1.cam_status(object)
                    session = 1
                    continue
                case "camexpose": #take light exposure with main ccd camera
                    duration = input('Duration in s?: ') #respond in float value
                    duration = float(duration)
                    image, object = maxim_menu1.cam_expose(object, duration)
                    session = 1
                    continue
                case "cooler": #controls the temperatures of the cooler
                    maxim_menu1.cam_cooler(object)
                    session = 1
                    continue
                case "temp": #queries for temp of the ccd camera 
                    maxim_menu1.cam_temp(object)
                    session = 1
                    continue
                case "list": #lists all possible commands at the given moment
                    print(options)
                    session = 1
                    continue
                case "warm": #doesnt actually turn on warm up (dont know how)
                    #instead this just turns the cooler off\
                    setpoint = input('What temp to warm to?:(as float)')
                    setpoint = float(setpoint)
                    maxim_menu1.warm(object, setpoint)
                    session = 1
                    continue
                case "deconvolve":
                    maxim_menu1.deconvolve(object, image)
                    session = 1
                    continue
                case "save":
                    maxim_menu1.save_image(image)
                    session = 1
                    continue
                case _: # when something is not entered correctly
                    print('Unknown command')
                    session = 1
                    continue
        case "n": #check to make sure all cameras are warmed / disconnected
            check = input("make sure all devices disconnected? (y/n): ")
            match check:
                case 'y':
                    session = 0
                    break
                case 'n': # if you decide to turn back, will prompt abt a command again
                    session = 1
                    continue
