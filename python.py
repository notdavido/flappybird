# Simple pygame program

# Import and initialize the pygame library
from random import seed
from random import randint
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    QUIT,
)
import math
import time
import pygame
from pygame import mixer 



pygame.init()



# Set up the drawing window
# pygame setup

maxx,maxy = 1280,720
screenx, screeny = maxx,maxy
radius = round(maxy/(11.5*2))

screen = pygame.display.set_mode((maxx, maxy),pygame.RESIZABLE, vsync=1)
clock = pygame.time.Clock()
running = True
dt = 0
ticks = 0
yacceleration = 0
yvelocity = 0
originalgravity = 14.5
gravity = 9.81

#playerstats
thePos = pygame.Vector2(200,500)

pipes = []
newlist = []

pipesy = []
pipenum = 0

# Run until the user asks to quit
running = True
color = 'red'
characterimage = pygame.image.load('python1/flappybird.png').convert_alpha() 
radiusmultiplier = maxy/250 #bigger num = smaller
imagesizex = radius*radiusmultiplier
characterimage = pygame.transform.scale(characterimage, (imagesizex, imagesizex)) #it sucks but the image is not perfect size so it needs to be slight more than radius



  
# Starting the mixer 
mixer.init() 
  
# Loading the song 

  
# Setting the volume 
mixer.music.set_volume(0.3) 
  
# Start playing the song 

speed = 1
speedchangepos = True
while running:
    
    # Did the user click the window close button?
    screen.fill((20, 150, 255))
    # charr = characterimage.get_rect()
    circle = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
    player = pygame.draw.circle(screen, (0,150,255,0), thePos, radius)
    rotated_image = pygame.transform.rotate(characterimage, -.1*yvelocity) 
    rotated_rect = rotated_image.get_rect(center=(player.x+radius, player.y+radius))

    showplayer = screen.blit(rotated_image, rotated_rect) #offset for image align


    
    # screen.blit(rotated_image, (showplayer.x,showplayer.y))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # print('press space')
                
                yvelocity = -390 * (screeny/720)
                mixer.music.load("python1/flappyswoosh.mp3") 
                mixer.music.play() 
                pass
    ticktime = False
    if ticks%105*1/speed  == 0: ##bigger = less frequent pipe spawn
        # ticktime = True
        pipenum += 1
        pipes.append(screenx)
        pipesy.append(randint(1, int(screeny*.75)))
        if speed >= 1.7:
            speedchangepos = False
        if speed <= 1:
            speedchangepos = True
        if speedchangepos:
            speed += .05
        else:
            speed -= .05
        print(speed)
    screenx,screeny = pygame.display.get_surface().get_size()
    radius = round(screeny/(11*2))

    # print(screenx,screeny)
    
    if pipes:
        if ticktime == False:
            for x in range(pipenum):
                # print(x)
                x = pipes.pop(0)
                y = pipesy.pop(0)
                newx = x-3*(speed*speed)
                if newx < 0:
                    pipenum-=1
                    continue
                pipe = pygame.draw.rect(screen, 'green', pygame.Rect(newx, 0, screenx/15, y))
                bottompipe = pygame.draw.rect(screen, 'green', pygame.Rect(newx, y+screeny*.24, screenx/15, 3000))
                ystandard = screeny/20
                xgreenstandard = screenx/15
                darkgreenparttop = pygame.draw.rect(screen, 'dark green', pygame.Rect(newx, pipe.y+pipe.height-ystandard, xgreenstandard, ystandard))
                darkgreenpartbottom = pygame.draw.rect(screen, 'dark green', pygame.Rect(newx, pipe.y+pipe.height+screeny*.24, xgreenstandard, ystandard))
                newlist.append(newx)
                pipesy.append(y)
            pipes = newlist
            # print(newlist)
    pygame.display.flip()
    # movement calcs

    if (player.y +radius*2)>= screeny:
        if player.y + radius*2 != screeny:
            thePos.y = screeny-radius
            yacceleration = 0
            yvelocity = 0
            gravity = 0
            # print('zeroed')
    
        
        
    else:
        gravity = originalgravity*(screeny/720)
        # print("gravity")
        
        

    
    gameover = False
    color = 'red'
    currentobstaclex = pipes[0]
    if player.x+player.width > pipes[0] and player.x < pipes[0] +screenx/15:
        originx = player.x+radius
        if originx> pipes[0] +screenx/15: # second half of circle (left)
            # print('second half')
            xdiff = abs(pipes[0]+screenx/15- originx)
            print(xdiff,radius)
            # print(xdiff, radius)
            ydiff = math.sqrt((radius*radius)-(xdiff*xdiff))
            # print(ydiff)
            posy = player.y+radius-ydiff
            # print('might be this')
            negy = posy+2*ydiff
            # print(negy,screeny)
            if negy > pipesy[0]+screeny*.24 or posy < pipesy[0]:
                color = 'blue'
                gameover = True
                # print('blue')
        if player.x + player.width > pipes[0] and originx < pipes[0]: #first half of circle
            # print('first half')
            # pipes[0]
            
            # xdiff = abs(pipes[0]- originx)
            # # print(xdiff, radius)
            # ydiff = math.sqrt((radius*radius)-(xdiff*xdiff))
            # posy = player.y-radius+ydiff
            # negy = posy+2*ydiff

            xdiff = abs(pipes[0]- originx)
            print(xdiff,radius)
            # print(xdiff, radius)
            ydiff = math.sqrt((radius*radius)-(xdiff*xdiff))
            # print(ydiff)
            posy = player.y+radius-ydiff
            # print('might be this')
            negy = posy+2*ydiff
            # print(negy,screeny)
            if negy > pipesy[0]+screeny*.24 or posy < pipesy[0]:
                color = 'blue'
                gameover = True
            
            # if posy < pipesy[0] or negy > pipesy[0]+screeny*.24:
            #     color = 'blue'
            #     gameover = True
                # print("s")
        if originx > pipes[0] and originx < pipes[0]+screenx/15: # middle section
            if player.y < pipesy[0] or player.y+player.height >pipesy[0]+screeny*.24:
                # time.sleep(1)
                color = 'blue'
                gameover = True
                # print("s")

    if gameover:
        mixer.music.load("python1/metalhit.mp3") 
        mixer.music.play() 
        # time.sleep(.2)
        pipesy.pop(0)
        pipes.pop(0)
        pipenum-=1
    thePos.y += yvelocity * dt
    yvelocity += gravity

    # Flip the display
    pygame.display.flip()
    dt = clock.tick(60) / 1000
    ticks += 1

    # print(dt)
    # print(pipes)

    # print("hi")
# Done! Time to quit.
pygame.quit()