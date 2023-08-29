import comtypes.client

#want to make a file that holds all of the settings for the OAG
#obviously this will be included on the final program...
# but for know they will sit here and be dormant
#or can be a package imported to final program
#should periodically check to make sure nothing is missing

def guide_movement(oag, *args):
    #movement
    max_moveX = oag.GuiderMaxMoveX
    max_moveY = oag.GuiderMaxMoveY
    min_moveX = oag.GuiderMinMoveX
    min_moveY = oag.GuiderMinMoveY
    speed_x = oag.GuiderXSpeed
    speed_y = oag.GuiderYSpeed
    moving = oag.GuiderMoving # read only
    return

def guide_aggressiveness(oag, *args):
    #aggressiveness
    oag_aggr_both = oag.GuiderAggressiveness
    oag_aggrX = oag.GuiderAggressivenessX
    oag_aggrY = oag.GuiderAggressivenessY
    return

def guide_temp(oag, *args):
    #temperature
    oag_ambient = oag.GuiderAmbientTemperature
    oag_temp = oag.GuiderTemperature # read only
    oag_tempset = oag.GuiderTemperatureSetpoint
    oag_coolstatus = oag.GuiderCoolerOn # read only
    oag_coolpower = oag.GuiderCoolerPower # read only
    return

def guide_track_settings(oag, *args):
    #tracking
    auto_select = oag.GuiderAutoSelectStar
    control_via = oag.GuideControlVia
    oag_calstate = oag.GuiderCalState # read only
    return
