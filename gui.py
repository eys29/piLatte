import os
import pygame # Import pygame graphics library
from pygame.locals import * #for event MOUSE variables
import RPi.GPIO as GPIO
import time
import math



#TODO uncomment these to show on piTFT
# os.putenv('SDL_VIDEODRIVER', 'fbcon') # Display on piTFT
# os.putenv('SDL_FBDEV', '/dev/fb0') #
# os.putenv('SDL_MOUSEDRV', 'TSLIB') # Track mouse clicks on piTFT
# os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')
#TODO set to False after debugging



GPIO.setmode(GPIO.BCM) # Set for GPIO numbering not pin numbers...

#### A motor #### 
GPIO.setup(5, GPIO.OUT) # AI1 5
GPIO.setup(6, GPIO.OUT) # AI2 6
GPIO.setup(13, GPIO.OUT) # PWM

#### B motor ####
GPIO.setup(20, GPIO.OUT) #BI1
GPIO.setup(21, GPIO.OUT) #BI2
# GPIO 16 is connected to PWMB which is used for speed control
GPIO.setup(16, GPIO.OUT) #PWM

duty_cycle = 50
freq = 50

pwmB = GPIO.PWM(16, 1)
pwmB.stop() # motor is stopped

pwmA = GPIO.PWM(13, 1)
pwmA.stop()

stopA = True
stopB = True

historyB = ["0 Stop"]
historyA = ["0 Stop"]

startTime = time.time()




### pygame setup ###

pygame.init()
pygame.mouse.set_visible(False)

WHITE = 255, 255, 255
BLACK = 0,0,0
RED = 255, 0, 0
GREEN = 0, 255, 0
screen = pygame.display.set_mode((320, 240))

screen.fill(BLACK) # Erase the Work space

stop_font = pygame.font.Font(None, 40)
stop_surface = stop_font.render("STOP", True, WHITE)
stop_rect = stop_surface.get_rect(center=(160,120))

resume_font = pygame.font.Font(None, 30)
resume_surface = resume_font.render("RESUME", True, WHITE)
resume_rect = resume_surface.get_rect(center=(160,120))

default_font = pygame.font.Font(None, 25)
quit_surface = default_font.render("Quit", True, WHITE)
quit_rect = quit_surface.get_rect(center=(280,210))

left_surface = default_font.render("Left History", True, WHITE)
left_rect = left_surface.get_rect(center=(50, 20))

right_surface = default_font.render("Right History", True, WHITE)
right_rect = left_surface.get_rect(center=(260, 20))

yForText = [50, 70, 90]

isStop = True

### pygame helpers ###

def drawStop():
    if isStop:
        pygame.draw.circle(screen, RED, (160, 120), 50)
        screen.blit(stop_surface, stop_rect)
    else:
        pygame.draw.circle(screen, GREEN, (160, 120), 50)
        screen.blit(resume_surface, resume_rect)

def drawQuit():
    screen.blit(quit_surface, quit_rect)
    
def drawLeft():
    screen.blit(left_surface, left_rect)
    sizeA = len(historyA)
    for i in range(min(3, sizeA)):
        text = historyA[sizeA-1-i]
        text_surface = default_font.render(text, True, WHITE)
        text_rect = text_surface.get_rect(center=(60, yForText[i]))
        screen.blit(text_surface, text_rect)
    
def drawRight():
    screen.blit(right_surface, right_rect)
    sizeB = len(historyB)
    for i in range(min(3, sizeB)):
        text = historyB[sizeB-1-i]
        text_surface = default_font.render(text, True, WHITE)
        text_rect = text_surface.get_rect(center=(265, yForText[i]))
        screen.blit(text_surface, text_rect)
        
drawStop()
drawQuit()
drawLeft()
drawRight()

### draw ###

pygame.display.flip()
while True:
    screen.fill(BLACK)
    drawStop()
    drawQuit()
    drawLeft()
    drawRight()
    pygame.display.flip()

    for event in pygame.event.get():
        if(event.type is MOUSEBUTTONDOWN):
            pos = pygame.mouse.get_pos()
        elif(event.type is MOUSEBUTTONUP):
            pos = pygame.mouse.get_pos()
            x,y = pos
            # center of circle is (160,120) and radius is 50
            if math.dist(pos, (160, 120)) < 50:
                isStop = not isStop
                pwmA.stop()
                pwmB.stop()
            # center of quit button is (280,210)
            if y > 200 and x > 240:
                quit()
                pwmA.stop()
                pwmB.stop()
    

