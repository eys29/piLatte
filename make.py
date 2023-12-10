import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# need to run sudo pigpiod before 
apin = 12
bpin = 13
GPIO.setup(apin, GPIO.OUT)
GPIO.setup(bpin, GPIO.OUT)
pwmA = GPIO.PWM(apin, 1)
pwmB = GPIO.PWM(bpin, 1)

pwmA.stop()
pwmB.stop()

freq = 50

sensor0pin = 20
sensor1pin = 21
sensor2pin = 17
GPIO.setup(sensor0pin, GPIO.IN)
GPIO.setup(sensor1pin, GPIO.IN)
GPIO.setup(sensor2pin, GPIO.IN)

# salt shakers
# 5, 6, 19, 26

#matcha
matchaPin = 5
GPIO.setup(matchaPin, GPIO.OUT) 
matchaGPIO = GPIO.PWM(matchaPin, freq) 

#coffee
coffeePin = 6
GPIO.setup(coffeePin, GPIO.OUT) 
coffeeGPIO = GPIO.PWM(coffeePin, freq) 

#cocoa
cocoaPin = 19
GPIO.setup(cocoaPin, GPIO.OUT) 
cocoaGPIO = GPIO.PWM(cocoaPin, freq) 

#sugar
sugarPin = 26
GPIO.setup(sugarPin, GPIO.OUT)
sugarGPIO = GPIO.PWM(sugarPin, freq) 

pumppin = 16
GPIO.setup(pumppin, GPIO.OUT) 

def pump():
    GPIO.output(pumppin, GPIO.LOW)
    time.sleep(1)
    GPIO.output(pumppin, GPIO.HIGH)
    time.sleep(.2)
    GPIO.output(pumppin, GPIO.LOW)

    time.sleep(13)

    GPIO.output(pumppin, GPIO.HIGH)
    time.sleep(.2)
    GPIO.output(pumppin, GPIO.LOW)




def configure1():
    print("matcha")
    matchaGPIO.start(0)
    matchaGPIO.ChangeDutyCycle(2)
    time.sleep(0.5)
    matchaGPIO.ChangeDutyCycle(0)
    for i in range(10):
        # matchaGPIO.ChangeDutyCycle(3)
        time.sleep(.1)
        # matchaGPIO.ChangeDutyCycle(2)
        time.sleep(.1)

    matchaGPIO.ChangeDutyCycle(7)
    time.sleep(0.5)
    matchaGPIO.ChangeDutyCycle(0)
    # print("coffee")
    # coffeeGPIO.start(0)
    # coffeeGPIO.ChangeDutyCycle(2)
    # time.sleep(0.5)
    # coffeeGPIO.ChangeDutyCycle(0)
    # coffeeGPIO.ChangeDutyCycle(7)
    # time.sleep(0.5)
    # coffeeGPIO.ChangeDutyCycle(0)
    
def configure2():
    cocoaGPIO.start(0)
    cocoaGPIO.ChangeDutyCycle(2)
    time.sleep(0.5)
    cocoaGPIO.ChangeDutyCycle(0)
    cocoaGPIO.ChangeDutyCycle(7)
    time.sleep(0.5)
    cocoaGPIO.ChangeDutyCycle(0)
    
    sugarGPIO.start(0)
    sugarGPIO.ChangeDutyCycle(2)
    sugarGPIO.ChangeDutyCycle(0)
    sugarGPIO.ChangeDutyCycle(7)
    sugarGPIO.ChangeDutyCycle(0)

teaspoon = .25

def dispenseMatcha():
    print("dispensing matcha")
    matchaGPIO.start(0)
    time.sleep(2)

    matchaGPIO.ChangeDutyCycle(2)
    time.sleep(0.5)
    matchaGPIO.ChangeDutyCycle(0)
    time.sleep(teaspoon)
    matchaGPIO.ChangeDutyCycle(9)
    time.sleep(0.5)
    matchaGPIO.ChangeDutyCycle(0)
    time.sleep(1)
    
def dispenseCoffee():
    print("dispensing coffee")

    coffeeGPIO.start(0)
    time.sleep(2)

    coffeeGPIO.ChangeDutyCycle(3)
    time.sleep(0.5)
    coffeeGPIO.ChangeDutyCycle(0)
    time.sleep(teaspoon)
    coffeeGPIO.ChangeDutyCycle(12)
    time.sleep(0.5)
    coffeeGPIO.ChangeDutyCycle(0)
    time.sleep(1)

def dispenseCocoa():
    print("dispensing cocoa")

    cocoaGPIO.start(0)
    time.sleep(2)

    cocoaGPIO.ChangeDutyCycle(2)
    time.sleep(0.5)
    cocoaGPIO.ChangeDutyCycle(0)
    time.sleep(teaspoon)
    cocoaGPIO.ChangeDutyCycle(8)
    time.sleep(0.5)
    cocoaGPIO.ChangeDutyCycle(0)
    time.sleep(1)


    
def dispenseSugar(i):
    print("dispensing sugar")

    sugarGPIO.start(0)
    time.sleep(2)

    sugarGPIO.ChangeDutyCycle(2)
    time.sleep(0.5)
    sugarGPIO.ChangeDutyCycle(0)
    time.sleep(i*.1)
    sugarGPIO.ChangeDutyCycle(8)
    time.sleep(0.5)
    sugarGPIO.ChangeDutyCycle(0)
    time.sleep(1)


def go_ccw():
    pwmB.start(6.5)
    pwmB.ChangeFrequency(freq)
    pwmA.start(6.5)
    pwmA.ChangeFrequency(freq)

def go_cw():
    pwmB.start(7.5)
    pwmB.ChangeFrequency(freq)
    pwmA.start(7.5)
    pwmA.ChangeFrequency(freq)


def stop():
    time.sleep(.2)
    pwmA.stop()
    pwmB.stop()
 


def makeLatte(matcha, coffee, cocoa, sugar):
    previousState = [0,0,0]
    senseStop = [0,0,0]
    done = [0,0,0]
    go_ccw()
    dontstop = True
    counter = 0
    while dontstop or counter > 10000:
        counter += 1
        sensor0 = GPIO.input(sensor0pin)
        sensor1 = GPIO.input(sensor1pin)
        sensor2 = GPIO.input(sensor2pin)
        # sensor 0 detects
        if previousState[0] and not sensor0:
            senseStop[0] = 1
        # sensor 1 detects
        if previousState[1] and not sensor1:
            senseStop[1] = 1
        # sensor 2 detects
        if previousState[2] and not sensor2:
            print("sensor 2")
            senseStop[2] = 1
            
        #dispensing 
        if senseStop[0] and (matcha or coffee) and not done[0]:
            stop()
            # dispense 
            if matcha: dispenseMatcha()
            if coffee: dispenseCoffee()
            done[0] = 1
            go_ccw()
            
        elif senseStop[1] and (sugar > 0 or cocoa) and not done[1]:
            stop()
            #dispense
            if cocoa: dispenseCocoa()
            if sugar > 0: dispenseSugar(sugar)
            done[1] = 1
            go_ccw()
        elif senseStop[2] and not done[2]:
            stop()
            pump()
            done[2] = 1
            dontstop = False
            break
            
        senseStop = [0,0,0]
            
        
        previousState[0] = sensor0
        previousState[1] = sensor1
        previousState[2] = sensor2
        
    go_ccw()
    time.sleep(2)
    stop()
    print("finished!")
    

# while 1:
#     print(GPIO.input(sensor2pin))

    
# makeLatte(matcha=0, coffee=0, cocoa=1, sugar=1)  
# go_cw()
# time.sleep(10)
# stop()

# configure1()

dispenseCoffee()


# pump()


