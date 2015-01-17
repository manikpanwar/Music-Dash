import pygame
import sys
from pygame import *
import textrect
import splash

def helpGen():
    GRAY = (128, 128, 128)
    GREEN = (0, 128, 0)
    DARKGRAY = (64, 64, 64)
    WHITE = (255, 255, 255)

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
    howToPlay = '* The goal is to eat up as many coins and avoid as many blocks as possible. Eating coins increases your score and hitting blocks decreases your score \n * The coins you earned will genate beautiful sound and the blocks you hit harm the generated sound'
    textBox = pygame.Rect(xmarginX, oriY + bigGap + xsmallGap, screenX - 2 * xmarginX, 200)
    textLong = textrect.render_textrect(howToPlay, xsmallfontObj, textBox, WHITE, GRAY)
    screen.blit(textLong, textBox)

    textSurfaceObj = smallfontObj.render('How to download the music', True, DARKGRAY, GRAY)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (130, oriY + 150)
    screen.blit(textSurfaceObj, textRectObj)

    howToD = '* Hit D on the keyboard to download'
    textBox = pygame.Rect(xmarginX, oriY + 170, screenX - 2 * xmarginX, 200)
    textLong = textrect.render_textrect(howToD, xsmallfontObj, textBox, WHITE, GRAY)
    screen.blit(textLong, textBox)

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
                splash.splash()
        pygame.display.update()
