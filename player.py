# MHacks project
# player class 

import pygame

class Player(object):

	def __init__(self, x, y):

		self.r = 20
		self.player = pygame.Surface((self.r*2, self.r*2))
		pygame.draw.circle(self.player, (0, 255, 0), (self.r, self.r), self.r, 0)
		self.rect = self.player.get_rect()
		self.rect.centerx = x
		self.rect.centery = y
		self.curRow = 0
