function guider_expose(oag, duration)
    Dim oag
    Set oag = CreateObject("MaxIm.CCDCamera")
    oag.LinkEnabled = True
    oag.GuiderExpose(duration)
End function