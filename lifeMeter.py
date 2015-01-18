# MHacks V

# Life Meter

import pygame
from obstaclesAndMusicNotes import Obstacle, MusicNote

class LifeMeter(object):

	def __init__(self):

		(self.width, self.height) = (106, 16) 
		self.meter = pygame.Surface((self.width, self.height))
		self.meter.set_colorkey((255, 255, 255))
		lineWidth = self.margin = 3 
		# pygame.draw.rect(self.meter, (0, 0, 0), (0, 0, self.width, self.height), 3)
		self.rect = self.meter.get_rect()
		self.lifePoints = 100

	def manageLife(self, obj=None):
		if isinstance(obj, MusicNote):
			self.lifePoints = min(self.lifePoints+5, 100)
		elif isinstance(obj, Obstacle):
			self.lifePoints = max(self.lifePoints-10, 0)
		else:
			self.lifePoints = max(self.lifePoints-5, 0)

	def drawBar(self): 
		(pygame.draw.rect(self.meter, (255, 255, 255), 
			(self.margin, self.margin, self.width-self.margin, self.height-self.margin*2), 0))
		(pygame.draw.rect(self.meter, (0, 255, 255), 
			(self.margin, self.margin, self.lifePoints, self.height-self.margin*2), 0))

	def checkGameOver(self):
		return self.lifePoints <= 0

	def draw(self, surface):
		self.drawBar()
		surface.blit(self.meter, self.rect)


