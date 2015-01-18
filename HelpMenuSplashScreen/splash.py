# ! /usr/bin/env python
# source: http://www.pygame.org/project-Splash+screen-1186-.html

import pygame
from pygame.locals import *
import time
import os, sys
from helpGen import HelpGen
from main import MusicDash

def splash():
    print('Splash load...')
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    pygame.init()
    pygame.font.init()

    GRAY = (128, 128, 128)
    GREEN = (0, 128, 0)
    BLUE = (0, 0, 255)

    # demension of screen
    screenX = 500
    screenY = 400
    screen = pygame.display.set_mode((screenX, screenY))
    pygame.display.set_caption('Runner Music Game v0.0 :)')

    # background fill color
    background = pygame.Surface(screen.get_size())
    background.fill(GRAY)
    screen.blit(background, (0,0))

    bigFontSize = 30
    smallFontSize = 20

    fontObj = pygame.font.Font('RobotoCondensed-Regular.ttf', bigFontSize)
    textSurfaceObj = fontObj.render('Runner Music Game v0.0!', True, GREEN, GRAY)
    textRectObj = textSurfaceObj.get_rect()
    offsetY = 70
    oriX = screenX // 2
    oriY = screenY // 2 - offsetY
    textRectObj.center = (oriX, oriY)
    screen.blit(textSurfaceObj, textRectObj)

    bigGap = 50
    smallfontObj = pygame.font.Font('RobotoCondensed-Regular.ttf', smallFontSize)
    textSurfaceObj = smallfontObj.render('New Game', True, BLUE, GRAY)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (250, oriY + bigGap)
    screen.blit(textSurfaceObj, textRectObj)

    smallGap = 30
    textSurfaceObj = smallfontObj.render('Help', True, BLUE, GRAY)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (250, oriY + bigGap + smallGap)
    screen.blit(textSurfaceObj, textRectObj)

    textSurfaceObj = smallfontObj.render('Quit', True, BLUE, GRAY)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (250, oriY + bigGap + smallGap * 2)
    screen.blit(textSurfaceObj, textRectObj)

    pygame.display.update()
    #time.sleep(5)

    while True: # main game loop
        for event in pygame.event.get():
            if (event.type == QUIT) or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP and event.key == K_h:
                helpGen.HelpGen()
                '''
                screen_h = pygame.display.set_mode((screenX, screenY))
                pygame.display.set_caption('General Help')
                background.fill(GRAY)
                screen.blit(background, (0,0))
                '''

        pygame.display.update()


splash()