import pygame
import os

import pygame.camera
import pygame.image

from pygame.locals import *

import time

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()

pygame.camera.init()

devices = pygame.camera.list_cameras()

if not devices:
    print("No devices, exiting")
device = pygame.camera.list_cameras()[0]

mysurf = pygame.Surface((640, 480), depth=32)
myrect = mysurf.get_rect()
clock = pygame.time.Clock()
running = True

level = 1

try:
    screen = pygame.display.set_mode((640, 480))
 
    pygame.display.flip()

    mysurf.fill((255, 255, 255))

    mycam = pygame.camera.Camera(device)
    #mycam.stop()
    mycam.start()

    count = 0
 
    while running:

        clock.tick(100)



        for evt in pygame.event.get():
            if evt.type == pygame.KEYDOWN and evt.key == pygame.K_ESCAPE or \
               evt.type == pygame.QUIT:
                running = False
                break

        mycam.get_image(mysurf)
        
#        if changed:
#            mysurf.fill((255, 255, 255))
     
        screen.blit(mysurf, (0, 0))
        pygame.display.flip()

        pygame.image.save(mysurf, "pyg%04d.png" % count)
        count += 1
finally:
    time.sleep(1)
    print("Stopping camera")
    mycam.stop()
    time.sleep(1)
    print("Camera stopped")   
    pygame.quit()  
