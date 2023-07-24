import time
import comtypes.client

#create COM object and connect
cam = comtypes.client.CreateObject("MaxIm.CCDCamera")
cam.LinkEnabled = True

# Check if the camera link is enabled
if cam.LinkEnabled == False:
    print('Camera 1 Failed to Start')
    quit()
elif cam.LinkEnabled == True:
    print('Camera 1 Connected, exposing...')
else:
    print('Unknown Error')
    quit()

#Exposing the Camera for 1 second
cam.Expose(1, 1, 0)

#Wait for the image to be ready
while cam.ImageReady == False:
    time.sleep(0.1) # save cpu whilst image prapres for download

#image saving
cam.SaveImage("File path ending in file name")

#shut down procedure
cam.Quit()
quit()

