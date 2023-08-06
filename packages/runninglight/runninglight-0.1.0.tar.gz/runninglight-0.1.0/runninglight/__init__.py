import RPi.GPIO as GPIO
import time
import datetime
import enum
import threading

class light_mode(enum.Enum):
    off = 1
    solid = 2
    blink_1sec = 3
    doubleblink_1sec = 4
    

class runninglightmanager:
    __mypin__ = 0
    __currentmode__ = light_mode.off
    __kill__ = False

    def __init__(self, pin):
        self.__mypin__ = pin

    def set_mode(self, mode: light_mode):
        self.__currentmode__ = mode

    def start(self):
        self.__kill__ = False
        t = threading.Thread(target=self.__continuouslyrun__)
        t.start()

    def __continuouslyrun__(self):
        while self.__kill__ == False:
            if (self.__currentmode__ == light_mode.off):
                GPIO.output(self.__mypin__, False)
                time.sleep(1)
            elif (self.__currentmode__ == light_mode.solid):
                GPIO.output(self.__mypin__, True)
                time.sleep(1)
            elif(self.__currentmode__ == light_mode.blink_1sec):
                GPIO.output(self.__mypin__, True)
                time.sleep(1)
                GPIO.output(self.__mypin__, False)
                time.sleep(1)
            elif(self.__currentmode__ == light_mode.doubleblink_1sec):
                GPIO.output(self.__mypin__, True)
                time.sleep(0.05)
                GPIO.output(self.__mypin__, False)
                time.sleep(0.05)
                GPIO.output(self.__mypin__, True)
                time.sleep(0.05)
                GPIO.output(self.__mypin__, False)
                time.sleep(0.05)
                time.sleep(1)

    
