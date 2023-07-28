import time
import comtypes.client

#create COM object and connect
cam = comtypes.client.CreateObject("MaxIm.CCDCamera")
cam.LinkEnabled = True

# Check if the camera link is enabled
if cam.LinkEnabled == False:
    print('Camera 1 Failed to Start')
elif cam.LinkEnabled == True:
    print('Camera 1 Connected, exposing...')
else:
    print('Unknown Error')

#Exposing the Camera for 1 second
cam.Expose(1, 1, 0)

#Wait for the image to be ready
while cam.ImageReady == False:
    time.sleep(0.1) # save cpu whilst image prapres for download

#image saving
# the r before the string makes it a raw string, couldn't save image w/o that
cam.SaveImage(r"C:\Users\NUC\OneDrive\Documents\MaxIm DL 6\image.fit")

#shut down procedure
cam.Quit()
quit()

