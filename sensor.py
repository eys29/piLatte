import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)

sensorpin = 21
GPIO.setup(sensorpin, GPIO.IN)


sense1 = 0

FIRST_SENSE = 0
NO_SENSE = 1
CHECK_SENSE = 2
ACTUAL_SENSE = 3

sensor1 = previous1 = 0
state1 = NO_SENSE
counter1 = sense1 = 0

while True:
    counter1 += 1
    sensor1 = GPIO.input(sensorpin)
    print(sensor1)
    # if state1 == NO_SENSE:
    #     if sensor1 and not previous1:
    #         state1 = FIRST_SENSE
    # elif state1 == FIRST_SENSE:
    #     print("first sense")
    #     counter1 = 1
    #     sense1 = 1
    #     state1 = CHECK_SENSE
    # elif state1 == CHECK_SENSE:
    #     sense1 += 1
    #     print("counter " + str(counter1) + " sensor " + str(sense1))
    #     if counter1 > 10 and abs(counter1-sense1) < 2:
    #         state1 = ACTUAL_SENSE
    # elif state1 == ACTUAL_SENSE:
    #     print("sensed!!")
    #     state1 = NO_SENSE

    # previous1 = sensor1
    time.sleep(0.1)
    
GPIO.cleanup()