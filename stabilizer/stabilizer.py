import pygame
import os

import pygame.camera
import pygame.image

from pygame.locals import *

import time

MAXD = 100

use_cam = True

os.environ['SDL_VIDEO_CENTERED'] = '1'

def find_offset_vector(oldsurf, newsurf, rectused, maxoffsx, maxoffsy, step, colordiff, sumdiff):
    oldpa = pygame.PixelArray(oldsurf)
    newpa = pygame.PixelArray(newsurf)


    buckets = {}

    iterations = 0

    for y in range(maxoffsy, rectused.height - maxoffsy, step):
        for x in range(maxoffsx, rectused.width - maxoffsx, step):
            r1 = oldpa[x, y] & 0xFF

            for dx in range(-maxoffsx, maxoffsx + 1):
                for dy in range(-maxoffsy, maxoffsy + 1):
                    iterations += 1
                    r2 = newpa[x + dx, y + dy] & 0xFF
                    if abs(r2 - r1) <= colordiff:
                        buckets[(dx, dy)] = buckets.setdefault((dx, dy), 0) + (colordiff - abs(r2 - r1) if sumdiff else 1)

    if len(buckets) > 0:
        lst = sorted(zip(buckets.values(), buckets.keys()))

        confidence = lst[-1][0] / iterations
        
        print(lst[-5:], iterations, confidence)

        if confidence > 0.0001 * colordiff or sumdiff:
            # TODO: confidence when sumdiff
            return lst[-1][1] # offset of the last=largest one

    return (0, 0)

def find_all_offsets(oldsurf, newsurf, rectused, maxoffsx, maxoffsy, step, colordiff, sumdiff):
    oldpa = pygame.PixelArray(oldsurf)
    newpa = pygame.PixelArray(newsurf)


    buckets = {}

    iterations = 0

    for y in range(maxoffsy, rectused.height - maxoffsy, step):
        for x in range(maxoffsx, rectused.width - maxoffsx, step):
            r1 = oldpa[x, y] & 0xFF

            for dx in range(-maxoffsx, maxoffsx + 1):
                for dy in range(-maxoffsy, maxoffsy + 1):
                    iterations += 1
                    r2 = newpa[x + dx, y + dy] & 0xFF
                    if abs(r2 - r1) <= colordiff:
                        buckets[(dx, dy)] = buckets.setdefault((dx, dy), 0) + (colordiff - abs(r2 - r1) if sumdiff else 1)

    
    lst = sorted(zip(buckets.values(), buckets.keys()))
    return lst



pygame.init()

pygame.camera.init()

devices = pygame.camera.list_cameras()

if not devices:
    print("No devices, exiting")
device = pygame.camera.list_cameras()[0]

mysurf = pygame.Surface((640, 480), depth=32)
oldsurf = pygame.Surface((640, 480), depth=32)
myrect = mysurf.get_rect()
clock = pygame.time.Clock()
running = True

level = 1

stabsurf = pygame.Surface((640, 480), depth=32)
font = pygame.font.Font(None, 36)

try:
    screen = pygame.display.set_mode((640, 480))
 
    pygame.display.flip()

    mysurf.fill((255, 255, 255))
    oldsurf.fill((0, 0, 0))

    if use_cam:
        mycam = pygame.camera.Camera(device)
        #mycam.stop()
        mycam.start()

    count = 0
    dx, dy = 0, 0
    while running:

        #clock.tick(100)



        for evt in pygame.event.get():
            if evt.type == pygame.KEYDOWN and evt.key == pygame.K_ESCAPE or \
               evt.type == pygame.QUIT:
                running = False
                break

        if use_cam:
            mycam.get_image(mysurf)
        else:
            try:
                mysurf = pygame.image.load("temp/pyg%04d.png" % count)
            except:
                pass

        
#        if changed:
#            mysurf.fill((255, 255, 255))


        if count > 0:
            if False:
                ndx, ndy = find_offset_vector(oldsurf, mysurf, myrect, 7, 7, 16, 10, False)
            else:
                v = find_all_offsets(oldsurf, mysurf, myrect, 7, 7, 16, 10, False)
                
                sm = sum(a[0] for a in v)
                mm = max(a[0] for a in v)
                #print(v)
                ndx, ndy = 0, 0

                ndx, ndy = v[-1][1]
                
                for a in v:
                    #ndx += a[1][0] * a[0]
                    #ndy += a[1][1] * a[0]
                    c = (255 * a[0]) // mm
                    pygame.draw.circle(mysurf, (c,c,c), (210 + a[1][0] * 10, 210 + a[1][1] * 10), 10 if (ndx == a[1][0] and ndy == a[1][1]) else 5)

                print(ndx, ndy)
                #ndx //= sm
                #ndy //= sm
            dx -= ndx
            dy -= ndy


            print (dx, dy)
            if not use_cam:
                stabsurf.fill((0, 0, 0))
                stabsurf.blit(mysurf, (dx, dy))

                text = font.render("%d %d %d %d" % (ndx, ndy, dx, dy), 1, (0, 0, 0))
                textpos = text.get_rect(left=100, top=100)
                stabsurf.blit(text, textpos)
            
                pygame.image.save(stabsurf, "temp/s%04d.png" % count)

        screen.fill((0, 0, 0))
        screen.blit(mysurf, (dx, dy))
        pygame.display.flip()

        oldsurf = mysurf.copy()

        ###pygame.image.save(mysurf, "pyg%04d.png" % count)
        count += 1
finally:

    if use_cam:
        time.sleep(1)
        print("Stopping camera")
        mycam.stop()
        time.sleep(1)
        print("Camera stopped")   
    pygame.quit()  
