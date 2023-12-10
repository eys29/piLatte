import os
import pygame # Import pygame graphics library
from pygame.locals import * #for event MOUSE variables
import RPi.GPIO as GPIO
import time

#TODO uncomment these to show on piTFT
os.putenv('SDL_VIDEODRIVER', 'fbcon') # Display on piTFT
os.putenv('SDL_FBDEV', '/dev/fb1') #
os.putenv('SDL_MOUSEDRV', 'TSLIB') # Track mouse clicks on piTFT
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')
#TODO set to False after debugging


##### bail button ##########

GPIO.setmode(GPIO.BCM) #bcm not pin numbers
#quit 
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
def GPIO17_callback(channel):
    pygame.quit()

    
GPIO.add_event_detect(17, GPIO.FALLING, callback=GPIO17_callback)
 
######################################
pygame.init()
pygame.mouse.set_visible(True)
WHITE = 255, 255, 255
BLACK = 0,0,0
screen = pygame.display.set_mode((320, 240))
quit_font = pygame.font.Font(None, 50)
touch_font = pygame.font.Font(None, 20)
screen.fill(BLACK) # Erase the Work space

quit_surface = quit_font.render("Quit", True, WHITE)
quit_rect = quit_surface.get_rect(center=(160,180))
screen.blit(quit_surface, quit_rect)
pygame.display.flip()

touches = []


while True:
    for event in pygame.event.get():
        if(event.type is MOUSEBUTTONDOWN):
            pos = pygame.mouse.get_pos()
        elif(event.type is MOUSEBUTTONUP):
            pos = pygame.mouse.get_pos()
            x,y = pos
            screen.fill(BLACK) # Erase the Work space
            message = "touch at " + "".join(str(pos))
            print(message)
            touches.append(pos)
            touch_surface = touch_font.render(message, True, WHITE)
            touch_rect = touch_surface.get_rect(center=(160, 120))
            screen.blit(touch_surface, touch_rect)
            screen.blit(quit_surface, quit_rect)
            pygame.display.flip()
            if y > 160:
                print(touches)
                screen.fill(BLACK)
                pygame.display.flip()
                pygame.quit()
                quit()
        
    


pygame.quit()
