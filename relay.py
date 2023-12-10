import os
import RPi.GPIO as GPIO
import time
import math

##### bail button ##########

GPIO.setmode(GPIO.BCM) #bcm not pin numbers
#quit 
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
def GPIO22_callback(channel):
    GPIO.output(13, GPIO.LOW)

    
GPIO.add_event_detect(22, GPIO.FALLING, callback=GPIO22_callback)

########################
#18, 23
pin = 23
GPIO.setup(pin, GPIO.OUT) 

GPIO.output(pin, GPIO.LOW)
time.sleep(1)
GPIO.output(pin, GPIO.HIGH)
time.sleep(.2)
GPIO.output(pin, GPIO.LOW)


time.sleep(13)

GPIO.output(pin, GPIO.HIGH)
time.sleep(.2)
GPIO.output(pin, GPIO.LOW)


