' Do we have to connect a camera to maxim to be able to use guider?
' that would be incredibly stupid, i will assume not
' Is using camera 1 as an autoguider, becuase we have two cameras initialized
' Should make note of settings somewhere, and then delete camera1 from settings

Dim oag
Set oag = CreateObject("MaxIm.CCDCamera")
oag.LinkEnabled = True

'make sure to check link
if Not oag.LinkEnabled Then
    wscript.echo "Failed to Start Guider Cam, quitting..."
    oag.Quit()
End if

wscript.echo "Guider connected, exposing"

oag.GuiderExpose 5

Do While oag.GuiderMoving
Loop

wscript.echo "Guider Exposure Complete"

'Shutdown Procedure
oag.Quit()

' Test Script for Guider #1, next is to test tracking methods
