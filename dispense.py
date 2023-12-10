# v1 - blink an LED
#
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM) # Set for GPIO numbering not pin numbers...
GPIO.setup(13, GPIO.OUT) # set GPIO 13 as output to blink LED
GPIO.setup(19, GPIO.OUT) # set GPIO 13 as output to blink LED
GPIO.setup(26, GPIO.OUT) # set GPIO 13 as output to blink LED



##### bail button ##########
#quit 
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
def GPIO22_callback(channel):
    pwm13.stop()
    GPIO.output(13, GPIO.LOW)
    quit()

    
GPIO.add_event_detect(22, GPIO.FALLING, callback=GPIO22_callback)

########## PWM #################
freq = 50
pwm13 = GPIO.PWM(26, freq) # pin 13 will generate a PWM pulse
pwm13.start(0)
time.sleep(2)

for i in range(5):
    print("forward " + str(i))
   # pwm13.stop()
    pwm13.ChangeDutyCycle(2)
    time.sleep(0.5)
    pwm13.ChangeDutyCycle(0)
    time.sleep(1)
    print("back " + str(i))
   # pwm13.stop()
    pwm13.ChangeDutyCycle(7)
    time.sleep(0.5)
    pwm13.ChangeDutyCycle(0)
    time.sleep(1)



pwm13.stop()




# servoname.ChangeDutyCycle(7)
# 	time.sleep(0.5)
# 	servoname.ChangeDutyCycle(0)
# 	time.sleep(1)
# 	servoname.ChangeDutyCycle(2)
# 	time.sleep(0.5)
# 	servoname.ChangeDutyCycle(0)
 

GPIO.cleanup()
