import comtypes.client
import maxim_menu1
import time

session = 1
object = None
while session == 1:
    command_bool = input('Operate Command? (y/n)')
    match command_bool:
        case "y":
            app = comtypes.client.CreateObject("MaxIm.Application")
            command_string = input('Command?:\n')
            match command_string:
                case "connect":
                    object = maxim_menu1.guider_connect()
                    session = 1
                    continue
                case "disconnect":
                    maxim_menu1.guider_disconnect()
                    session = 1
                    continue
                case "expose":
                    duration = input('Duration in s?: ')
                    duration = float(duration)
                    maxim_menu1.guider_expose(duration, object)
                    session = 1
                    continue
                case "calibrate":
                    duration = input('Duration in s?: ')
                    duration = float(duration)
                    maxim_menu1.guider_calibrate(duration)
                    session = 1
                    continue
                case "calstate":
                    maxim_menu1.guider_calstate
                    session = 1
                    continue
                case "guidestar":
                    maxim_menu1.guidestar_coords()
                    session = 1
                    continue
        case "n":
            check = input("make sure all devices disconnected? (y/n): ")
            match check:
                case 'y':
                    session = 0
                    break
                case 'n':
                    session = 1
                    continue
