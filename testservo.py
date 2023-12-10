import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.OUT)

servo1 = GPIO.PWM(13, 50)
servo1.start(0)
time.sleep(2)

servo1.ChangeDutyCycle(7)
time.sleep(0.5)
servo1.ChangeDutyCycle(0)
time.sleep(1.5)

servo1.ChangeDutyCycle(2)
time.sleep(2)

servo1.stop()
GPIO.cleanup()


