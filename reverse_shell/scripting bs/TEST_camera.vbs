Dim cam ' "The" Camera object
Set cam = CreateObject("MaqxIm.CCDCamera")
cam.LinkEnabled = True 

if Not cam.LinkEnabled Then 
    wscript.echo "Failed to start camera."
    Close()
End if

wscript.echo "Camera is ready, exposing"

cam.Expose 1, 1, 0

Do While Not cam.ImageReady
Loop

cam.SaveImage "Image.fit"
wscript.echo "Exposure is done, Image saved as Image.fit"

' Shutdown Procedure
cam.Quit()
Close()