import RPi.GPIO as GPIO
import time
import pigpio

GPIO.setmode(GPIO.BCM)

# need to run sudo pigpiod before 
apin = 12
bpin = 13
#75000 for ccw 
#85000 for cw
calibrate = 70000
cw = 60000
ccw = 78000

direction = cw
GPIO.setup(apin, GPIO.OUT)
GPIO.setup(bpin, GPIO.OUT)

pwmA = GPIO.PWM(apin, 1)
pwmB = GPIO.PWM(bpin, 1)

pwmA.stop()
pwmB.stop()

duty_cycle = 8
freq = 50


def calibrate():
    pwmB.start(7)
    pwmB.ChangeFrequency(freq)
    pwmA.start(7)
    pwmA.ChangeFrequency(freq)
    
def go_cw():
    pwmB.start(6)
    pwmB.ChangeFrequency(freq)
    pwmA.start(6)
    pwmA.ChangeFrequency(freq)

def go_ccw():
    pwmB.start(8)
    pwmB.ChangeFrequency(freq)
    pwmA.start(8)
    pwmA.ChangeFrequency(freq)


def stop():
    pwmA.stop()
    pwmA.stop()
    
    
go_ccw()
time.sleep(10)
stop()

# go_cw()
# time.sleep(5)
# stop()
# go_ccw()
# time.sleep(5)
# stop()