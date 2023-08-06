Running Light Control
======================
A light-weight package for controlling a raspberry-pi connected LED running light.  
### Example code:

    import RPi.GPIO as GPIO
    import runninglight
    import time


    #Pin for the light
    MPIN = 3

    #set up
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(MPIN, GPIO.OUT)

    #create
    rlm = runninglight.runninglightmanager(MPIN)

    #run
    rlm.set_mode(runninglight.light_mode.doubleblink_1sec)
    rlm.start()
    print("Started!")