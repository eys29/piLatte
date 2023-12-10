import os
import pygame # Import pygame graphics library
from pygame.locals import * #for event MOUSE variables
import RPi.GPIO as GPIO
import time
import math
# from make import *
import threading

os.putenv('SDL_VIDEODRIVER', 'fbcon') # Display on piTFT
os.putenv('SDL_FBDEV', '/dev/fb0') #
os.putenv('SDL_MOUSEDRV', 'TSLIB') # Track mouse clicks on piTFT
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

####### MAKE #####


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

teaspoon = 1

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
 


def makeLatte(e, matcha, coffee, cocoa, sugar):
    e.clear()
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
    time.sleep(1)
    stop()
    print("finished!")
    e.set()
   







    
#### pygame ###


START = 0
FLAVOR = 1
SWEET = 2
MAKE = 3
ANIMATE = 4
DONE = 5

state = START

pygame.init()
pygame.mouse.set_visible(False)

background_color = 147, 184, 123
BLACK = 0,0,0
RED = 255, 0, 0
button_color = 178, 201, 163
width = 320
height = 240
center_x = int(width / 2)
center_y = int(height / 2)
screen = pygame.display.set_mode((width, height))

screen.fill(background_color) # Erase the Work space

##### bail button ##########

GPIO.setmode(GPIO.BCM) #bcm not pin numbers
#quit 

dontquit = True
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
def GPIO22_callback(channel):
    matchaGPIO.stop()
    coffeeGPIO.stop()
    cocoaGPIO.stop()
    sugarGPIO.stop()
    GPIO.output(pumppin, GPIO.LOW)
    GPIO.cleanup()
    print("quit gpios")
    global dontquit
    dontquit = False
    

    
GPIO.add_event_detect(22, GPIO.FALLING, callback=GPIO22_callback)

#shutdown 
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
def GPIO27_callback(channel):
    matchaGPIO.stop()
    coffeeGPIO.stop()
    cocoaGPIO.stop()
    sugarGPIO.stop()
    GPIO.output(pumppin, GPIO.LOW)
    GPIO.cleanup()
    global dontquit
    dontquit = False
    os.system('sudo shutdown -h now')
    
GPIO.add_event_detect(27, GPIO.FALLING, callback=GPIO27_callback)

########################
   
class Text:
    letter_size = (15, 20)
    font = pygame.font.SysFont("quicksandlight", 25)

    def __init__(self, text, center):
        self.surface = self.font.render(text, True, BLACK)
        self.rect = self.surface.get_rect(center=center)
        self.text = text
        self.center = center
        self.calculateTextBox()
        
        
    def calculateTextBox(self):
        length = len(self.text)
        cx, cy = self.center
        self.width = length * self.letter_size[0]
        self.height = self.letter_size[1]
        half_width = int(self.width / 2)
        half_height = int(self.height / 2)
        self.xs = (cx-half_width, cx+half_width)
        self.ys = (cy-half_height, cy+half_height)
        
    def buttonHit(self, mouse):
        x, y = mouse
        return x > self.xs[0]-5 and x < self.xs[1]+5 and y > self.ys[0]-5 and y < self.ys[1]+5
        
    def drawButton(self):
        pygame.draw.rect(screen, button_color, pygame.Rect(self.xs[0]-5, self.ys[0]-5, self.width+10, self.height+10))
        self.draw()

        
    def draw(self):
        screen.blit(self.surface, self.rect)

            
texts = {}
texts["welcome"] = Text("Welcome to MatchaMaker!", (center_x, 100))       

texts["start"] = Text("START", (center_x, 150))

texts["flavor"] = Text("Pick a latte flavor:", (center_x, 50))
texts["matcha"] = Text("Matcha", (center_x, 100))
texts["coffee"] = Text("Coffee", (center_x, 150))
texts["cocoa"] = Text("Hot Cocoa", (center_x, 200))

texts["sweetness"] = Text("Pick a sweetness level:", (center_x, 100))

sugar_levels = []
space = (width-60) / 4
sugar_coords = [25, space + 15, 2*space + 15, 3*space + 15, 4*space + 20]
for i in range(5):
    sugar_levels.append(25*i)
    texts[sugar_levels[i]] = Text(str(sugar_levels[i]) + "%", (sugar_coords[i], 150))

texts["make"] = Text("Preparing your latte...", (center_x, 100))

frames = []

for i in range(150):
    num = ""
    if i < 10: num = "00" + str(i)
    elif i < 100: num = "0" + str(i)
    else: num = str(i)
    img = pygame.image.load("/home/pi/final/animation/frame_" + num + "_delay-0.03s.gif")
    img = pygame.transform.scale(img, (width*2, height*2))
    imgrect = img.get_rect(center=(center_x, center_y))
    frames.append((img, imgrect))



def drawStart():
    screen.fill(background_color)
    texts["welcome"].draw()
    texts["start"].drawButton()
    pygame.display.flip()

def drawFlavor():
    screen.fill(background_color)
    texts["matcha"].drawButton()
    texts["coffee"].drawButton()
    texts["cocoa"].drawButton()
    texts["flavor"].draw()
    pygame.display.flip()

def drawSweet():
    screen.fill(background_color)
    texts["sweetness"].draw()

    for i in range(len(sugar_levels)):
        texts[sugar_levels[i]].drawButton()
    pygame.display.flip()
    
def drawMake():
    screen.fill(background_color)
    texts["make"].draw()
    pygame.display.flip()
    
def drawAnimation(i):
    screen.blit(frames[i][0], frames[i][1]) 
    pygame.display.flip()
    time.sleep(.05)


    
        
def animate(e):
    starttime = time.time()
    currenttime = time.time()
    animation_counter = 0
    while not e.isSet():
        currenttime = time.time()
        animation_counter = (animation_counter + 1) % 150
        drawAnimation(animation_counter)
  
sugar_dispense = matcha_dispense = coffee_dispense = cocoa_dispense = 0
      


while dontquit:
    screen.fill(background_color) # Erase the Work space

    if state == START:
        drawStart()
        sugar_dispense = matcha_dispense = coffee_dispense = cocoa_dispense = 0
        for event in pygame.event.get():
            if(event.type is MOUSEBUTTONDOWN):
                pos = pygame.mouse.get_pos()
            elif(event.type is MOUSEBUTTONUP):
                pos = pygame.mouse.get_pos()
                
                message = "touch at " + "".join(str(pos))
                print(message)

                start = texts["start"]
                if start.buttonHit(pos):
                    print("clicked start")
                    state = FLAVOR
                    
    if state == FLAVOR:
        drawFlavor()
        for event in pygame.event.get():
            if(event.type is MOUSEBUTTONDOWN):
                pos = pygame.mouse.get_pos()
            elif(event.type is MOUSEBUTTONUP):
                pos = pygame.mouse.get_pos()
                
                message = "touch at " + "".join(str(pos))
                print(message)

                if texts["matcha"].buttonHit(pos):
                    print("clicked matcha")
                    matcha_dispense = 1
                    state = SWEET
                elif texts["coffee"].buttonHit(pos):
                    print("clicked coffee")
                    coffee_dispense = 1
                    state = SWEET
                elif texts["cocoa"].buttonHit(pos):
                    print("clicked cocoa")
                    cocoa_dispense = 1
                    state = SWEET
                
    if state == SWEET:
        drawSweet()
        for event in pygame.event.get():
            if(event.type is MOUSEBUTTONDOWN):
                pos = pygame.mouse.get_pos()
            elif(event.type is MOUSEBUTTONUP):
                pos = pygame.mouse.get_pos()
                
                message = "touch at " + "".join(str(pos))
                print(message)

                for i in range(len(sugar_levels)):
                    sugar = texts[sugar_levels[i]]
                    if sugar.buttonHit(pos):
                        print("clicked sugar" + str(sugar_levels[i]))
                        sugar_dispense = i
                        state = MAKE
    if state == MAKE:
        print("in make state")
        e = threading.Event()
        thread_animate = threading.Thread(target=animate, args=(e,))
        thread_make = threading.Thread(target=makeLatte, args=(e, matcha_dispense, coffee_dispense, cocoa_dispense, sugar_dispense))
        
        thread_make.start()
        thread_animate.start()
        thread_make.join()
        thread_animate.join()
        # makeLatte(matcha_dispense, coffee_dispense, cocoa_dispense, sugar_dispense)
        state = DONE
        
    
    if state == DONE:
        # GPIO.cleanup()
        state = START
        
screen.fill(BLACK) # Erase the Work space
pygame.display.flip()
pygame.quit()