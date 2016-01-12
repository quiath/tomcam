import pygame
import pygame.camera
import pygame.image

import datetime

# written by Quiath, 2016

CamW = 160
CamH = 120    

def rgb_filter1D(s, i, rx, ry):
    v = int(s[i])

    if rx == 1 != ry:
        # green ru
        g = v
        r = (int(s[i - CamW]) + int(s[i + CamW])) // 2
        b = (int(s[i - 1]) + int(s[i + 1])) // 2
    elif rx == 0 != ry:
        # green lb
        g = v
        b = (int(s[i - CamW]) + int(s[i + CamW])) // 2
        r = (int(s[i - 1]) + int(s[i + 1])) // 2
    elif rx == 0 == ry:
        b = v
        r = (int(s[i - CamW - 1]) + int(s[i + CamW + 1])) // 2
        g = (int(s[i - 1]) + int(s[i + 1])) // 2
    else:
        r = v
        b = (int(s[i - CamW - 1]) + int(s[i + CamW + 1])) // 2
        g = (int(s[i - 1]) + int(s[i + 1])) // 2
       
    return (r, g, b)

def rgb_filter_almost2D(s, i, rx, ry):
    v = int(s[i])

    if rx == 1 != ry:
        # green ru
        g = v
        r = (int(s[i - CamW]) + int(s[i + CamW])) // 2
        b = (int(s[i - 1]) + int(s[i + 1])) // 2
    elif rx == 0 != ry:
        # green lb
        g = v
        b = (int(s[i - CamW]) + int(s[i + CamW])) // 2
        r = (int(s[i - 1]) + int(s[i + 1])) // 2
    elif rx == 0 == ry:
        b = v
        r = (int(s[i - CamW - 1]) + int(s[i + CamW + 1])) // 2
        g = (int(s[i - 1]) + int(s[i + 1]) +
                 int(s[i - CamW]) + int(s[i + CamW])) // 4
    else:
        r = v
        b = (int(s[i - CamW - 1]) + int(s[i + CamW + 1])) // 2
        g = (int(s[i - 1]) + int(s[i + 1]) +
                 int(s[i - CamW]) + int(s[i + CamW])) // 4                        
        
    return (r, g, b)

def rgb_filter_raw(s, i, rx, ry):
    v = int(s[i])

    if rx == 1 != ry:
        # green ru
        g = v
        r = 0
        b = 0
    elif rx == 0 != ry:
        # green lb
        g = v
        b = 0
        r = 0
    elif rx == 0 == ry:
        b = v
        r = 0
        g = 0
    else:
        r = v
        b = 0
        g = 0                        
        
    return (r, g, b)

def rgb_filter_max(s, i, rx, ry):
    v = int(s[i])

    if rx == 1 != ry:
        # green ru
        g = v
        r = max(int(s[i - CamW]), int(s[i + CamW]))
        b = max(int(s[i - 1]), int(s[i + 1]))
    elif rx == 0 != ry:
        # green lb
        g = v
        b = max(int(s[i - CamW]), int(s[i + CamW]))
        r = max(int(s[i - 1]), int(s[i + 1]))
    elif rx == 0 == ry:
        b = v
        r = max(int(s[i - CamW - 1]), int(s[i + CamW + 1]))
        g = max(int(s[i - 1]), int(s[i + 1]),
                 int(s[i - CamW]), int(s[i + CamW]))
    else:
        r = v
        b = max(int(s[i - CamW - 1]), int(s[i + CamW + 1]))
        g = max(int(s[i - 1]), int(s[i + 1]),
                 int(s[i - CamW]), int(s[i + CamW]))
        
    return (r, g, b)

def bw_filter_fast(s, i, rx, ry):
    v = int(s[i]) << 1
    v += int(s[i - 1]) + int(s[i + 1])
    v = v >> 2
    return (v, v, v)

def bw_filter_block(s, i, rx, ry):
    v = int(s[i]) + int(s[i - CamW]) + int(s[i - 1]) + int(s[i - CamW - 1])
    v = v >> 2
    return (v, v, v)

def main():
    try:
        pygame.init()
        pygame.camera.init()
        cam = None
        camlist = pygame.camera.list_cameras()

        if len(camlist) < 1:
            print("No camera found")
            return

        cam = pygame.camera.Camera(camlist[0], (CamW, CamH))
        cam.start()
        screen_width = 640
        screen_height = 480

        screen = pygame.display.set_mode([screen_width, screen_height])

        clock = pygame.time.Clock()

        surf = pygame.Surface((CamW, CamH))
        
        done = False

        the_filter = rgb_filter1D
        the_name = "filter1D"

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        done = True
                    elif event.key == pygame.K_SPACE:
                        ds = datetime.datetime.isoformat(datetime.datetime.now())[:19]
                        ds = ds.replace(':', '_')
                        pygame.image.save(screen, the_name + "_" + ds + ".bmp")
                    elif event.key == pygame.K_1:
                        the_filter = rgb_filter1D
                        the_name = "filter1D"                
                    elif event.key == pygame.K_2:
                        the_filter = rgb_filter_almost2D
                        the_name = "filter2D"                
                    elif event.key == pygame.K_3:
                        the_filter = rgb_filter_max
                        the_name = "filterMax"
                    elif event.key == pygame.K_0:
                        the_filter = rgb_filter_raw
                        the_name = "filterRaw"
                    elif event.key == pygame.K_9:
                        the_filter = bw_filter_fast
                        the_name = "filterBW"             
                    elif event.key == pygame.K_8:
                        the_filter = bw_filter_block
                        the_name = "filterBlock"             
            
            # get the image from the camera            
            t0 = datetime.datetime.now()
            s = cam.get_raw()
            t1 = datetime.datetime.now()

            # show the length of the raw buffer, its first bytes and cam read time
            print(len(s), [int(a) for a in s[:10]], t1 - t0 )

            pa = pygame.PixelArray(surf)

            scale = 4

            t0 = datetime.datetime.now()

            #   0 1
            # 0 B G
            # 1 G R 
            x = 0
            y = 0
            for i, ch in enumerate(s):
                if not(x < 1 or y < 1 or x >= CamW - 1 or y >= CamH - 1):
                    rx , ry = x % 2, y % 2
               
                    pa[x, y] = the_filter(s, i, rx, ry)
                    
                x += 1
                if x == CamW:
                    x, y  = 0, y + 1
                
            del pa

            t1 = datetime.datetime.now()
            print("Filter loop time =", t1 - t0)
            
            surf_sc = pygame.transform.scale(surf,
                        (surf.get_size()[0] * scale, surf.get_size()[1] * scale))
            

            screen.blit(surf_sc, (0, 0))
            clock.tick(20)
            pygame.display.flip()

    finally:
        if cam:
            cam.stop()
        pygame.quit()


if __name__ == "__main__":
    main()

    
