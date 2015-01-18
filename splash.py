# ! /usr/bin/env python
# source: http://www.pygame.org/project-Splash+screen-1186-.html

import pygame
from pygame.locals import *
import time
import os, sys
import textrect
from helpGen import HelpGen
from main import MusicDash
import thread

def displayHelp():
    GRAY = (255, 255, 255)
    GREEN = (66, 255, 35)
    DARKGRAY = (64, 64, 64)
    WHITE = (0, 0, 255)

    # demension of screen
    screenX = 500
    screenY = 400
    screen = pygame.display.set_mode((screenX, screenY))
    pygame.display.set_caption('General Help')

    # background fill color
    background = pygame.Surface(screen.get_size())
    background.fill(GRAY)
    screen.blit(background, (0,0))

    bigFontSize = 30
    smallFontSize = 20
    pygame.font.init()

    fontObj = pygame.font.Font('RobotoCondensed-Regular.ttf', bigFontSize)
    textSurfaceObj = fontObj.render('General Help', True, GREEN, GRAY)
    textRectObj = textSurfaceObj.get_rect()
    offsetY = 120
    oriX = screenX // 2
    oriY = screenY // 2 - offsetY
    textRectObj.center = (oriX, oriY)
    screen.blit(textSurfaceObj, textRectObj)

    bigGap = 30
    marginX = 70
    smallfontObj = pygame.font.Font('RobotoCondensed-Regular.ttf', smallFontSize)
    textSurfaceObj = smallfontObj.render('How to play', True, DARKGRAY, GRAY)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (marginX, oriY + bigGap)
    screen.blit(textSurfaceObj, textRectObj)

    xsmallGap = 15
    xsmallFontSize = 12
    xmarginX = 40
    xsmallfontObj = pygame.font.Font('RobotoCondensed-Regular.ttf', xsmallFontSize)
    howToPlay = '* The goal is to gather as many music notes and avoid as many blocks as possible. Gathering music notes increases your score and hitting rests decreases your score \n\
     * The music notes you collect will generate beautiful sound.'
    textBox = pygame.Rect(xmarginX, oriY + bigGap + xsmallGap, screenX - 2 * xmarginX, 200)
    textLong = textrect.render_textrect(howToPlay, xsmallfontObj, textBox, WHITE, GRAY)
    screen.blit(textLong, textBox)

    # textSurfaceObj = smallfontObj.render('How to download the music', True, DARKGRAY, GRAY)
    # textRectObj = textSurfaceObj.get_rect()
    # textRectObj.center = (130, oriY + 150)
    # screen.blit(textSurfaceObj, textRectObj)

    # howToD = '* Hit D on the keyboard to download'
    # textBox = pygame.Rect(xmarginX, oriY + 170, screenX - 2 * xmarginX, 200)
    # textLong = textrect.render_textrect(howToD, xsmallfontObj, textBox, WHITE, GRAY)
    # screen.blit(textLong, textBox)

    textSurfaceObj = smallfontObj.render('Back to Main Menu (B)', True, DARKGRAY, GRAY)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (370, oriY + 220)
    screen.blit(textSurfaceObj, textRectObj)

    pygame.display.update()

    while True: # main game loop
        for event in pygame.event.get():
            if (event.type == QUIT) or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP and K_b:
                splash()
        pygame.display.update()

def startGame():
    thread.start_new_thread(MusicDash().run(),())

def splash():
    print('Splash load...')
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    pygame.init()
    pygame.font.init()

    GRAY = (255, 255, 255)
    GREEN = (66, 255, 35)
    BLUE = (0, 0, 255)

    # demension of screen
    screenX = 500
    screenY = 400
    screen = pygame.display.set_mode((screenX, screenY))
    pygame.display.set_caption('Music Dash v0.0 :)')

    # background fill color
    background = pygame.Surface(screen.get_size())
    background.fill(GRAY)
    screen.blit(background, (0,0))

    bigFontSize = 30
    smallFontSize = 20

    fontObj = pygame.font.Font('RobotoCondensed-Regular.ttf', bigFontSize)
    textSurfaceObj = fontObj.render('Music Dash!', True, GREEN, GRAY)
    textRectObj = textSurfaceObj.get_rect()
    offsetY = 70
    oriX = screenX // 2
    oriY = screenY // 2 - offsetY
    textRectObj.center = (oriX, oriY)
    screen.blit(textSurfaceObj, textRectObj)

    bigGap = 50
    smallfontObj = pygame.font.Font('RobotoCondensed-Regular.ttf', smallFontSize)
    textSurfaceObj = smallfontObj.render('New Game(n)', True, BLUE, GRAY)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (250, oriY + bigGap)
    screen.blit(textSurfaceObj, textRectObj)

    smallGap = 30
    textSurfaceObj = smallfontObj.render('Help(h)', True, BLUE, GRAY)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (250, oriY + bigGap + smallGap)
    screen.blit(textSurfaceObj, textRectObj)

    textSurfaceObj = smallfontObj.render('Quit(q)', True, BLUE, GRAY)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (250, oriY + bigGap + smallGap * 2)
    screen.blit(textSurfaceObj, textRectObj)

    pygame.display.update()
    #time.sleep(5)

    while True: # main game loop
        for event in pygame.event.get():
            if ((event.type == QUIT) or (event.type == KEYUP and event.key == K_ESCAPE)
                            or (event.type == KEYUP and event.key == K_q)):
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP and event.key == K_h:
                displayHelp()
            elif event.type == KEYUP and event.key == K_n:
                pygame.quit()
                try:
                    sys.exit()
                except:
                    startGame()
        pygame.display.update()


splash()

