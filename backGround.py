# ! /usr/bin/env python

import pygame
from pygame.locals import *
import time
import os, sys

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()
pygame.font.init()

GRAY = (128, 128, 128)
GREEN = (96, 96, 96)
BLUE = (0, 0, 255)

# dimension of screen
screenX = 500
screenY = 500
oriX = screenX // 2
oriY = screenY // 2
center = (oriX, oriY)
leftBottom = (0, screenY)
rightBottom = (screenX, screenY)
screen = pygame.display.set_mode((screenX, screenY))
pygame.display.set_caption('Runner Music Game v0.0 :)')

line_w = 2
# background fill color
background = pygame.Surface(screen.get_size())
background.fill(GRAY)
screen.blit(background, (0,0))
pygame.draw.line(screen, GREEN, center, leftBottom, line_w)
pygame.draw.line(screen, GREEN, center, rightBottom, line_w)

color = [(255, 102, 102),
        (255, 178, 102),
        (255, 255, 102),
        (178, 255, 102),
        (102, 255, 102),
        (102, 255, 178)]
lenColor = len(color)
offset = 1
period = 16
def rainbow(start, period):
    for i in range(period):
        change = i * i * offset
        change2 = (i + 1) * (i + 1) * offset
        pygame.draw.polygon(screen, color[((-1)*i + start) % lenColor], ((oriX - change, oriY + change), (oriX + change, oriY + change), (oriX + change2, oriY + change2), (oriX - change2, oriX + change2)))

for tm in range (100):
    rainbow(tm, 16)
    time.sleep(0.5)
    pygame.display.update()

def foo():
    while True: # main game loop
        for event in pygame.event.get():
            if (event.type == QUIT) or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
        pygame.display.update()

foo()