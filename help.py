import os
import pygame # Import pygame graphics library
from pygame.locals import * #for event MOUSE variables
import RPi.GPIO as GPIO
import time
import math

GPIO.setmode(GPIO.BCM) # Set for GPIO numbering not pin numbers...

GPIO.setup(22, GPIO.OUT) # PWM
GPIO.setup(16, GPIO.OUT) #PWM
pwmB = GPIO.PWM(16, 1)
pwmB.stop() # motor is stopped

pwmA = GPIO.PWM(22, 1)
pwmA.stop()