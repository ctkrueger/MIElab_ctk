Dim oag
Set oag = CreateObject("MaxIm.CCDCamera")
oag.LinkEnabled = True

' Check Link Anyways
if Not oag.LinkEnabled then
    wscript.echo "Failed to start guider, quitting..."
    oag.Quit()
    Close()
End if

wscript.echo "Guider Connected, looking for guide star"

' Auto Selecting Star
oag.GuiderAutoSelectStar = True
' Exposing for three seconds
oag.GuiderExpose(3)

Do While oag.GuiderMoving = True
    Loop
End While

'If guide star was found, the coordinates should be bigger than 0
x = oag.GuiderXStarPosition
y = oag.GuiderYStarPosition

wscript.echo x
wscript.echo y 

'Shutdown Procedure
oag.Quit()
Close()

' Test Script for Guider #2, next is to test calibration