Dim oag
Set oag = CreateObject("MaxIm.CCDCamera")
oag.LinkEnabled = True

' Check Link Anyways
If Not oag.LinkEnabled then
    wscript.echo "Failed to start guider, quitting..."
    oag.Quit()
    Close()
End If

wscript.echo "Link Enabled, Checking for Calibration Code..."

calibration = oag.GuiderCalState

If calibration = 0 Then
    wscript.echo "Guider not calibrated, beginning calibration"
    oag.GuiderCalibrate(3) ' 3 second exposures for calibration (within recommended range)
ElseIf calibration = 1 Then
    wscript.echo "Guider Calibrating from previous session, wait..."
    Do While oag.GuiderMoving = True
        Loop
    End While
End If

Do While oag.GuiderMoving = True
    Loop
End While

If oag.GuiderCalState = 2 Then
    wscript.echo "Guider Calibrated Successfully, shutting down"
ElseIf oag.GuiderCalState = 3 Then
    wscript.echo "Guider Calibration Failed, shutting down"
End If

'Shutdown Procedure Maybe
oag.Quit()
Close()

