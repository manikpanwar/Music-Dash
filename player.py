# MHacks project
# player class 

import pygame

class Player(object):

	def __init__(self, x, y):

		self.r = 20
		# self.player = pygame.Surface((self.r*2, self.r*2))
		# pygame.draw.circle(self.player, (0, 255, 0), (self.r, self.r), self.r, 0)
		# self.rect = self.player.get_rect()
		# self.player.set_colorkey((0, 0, 0))
		self.curRow = 0
		self.playerImage = pygame.image.load("pikachuBack.png") 
		self.playerImage.convert_alpha()
		self.imageRect = self.playerImage.get_rect()
		(self.imgWidth, self.imgHeight) = self.imageRect.size
		self.player = pygame.Surface((self.imgWidth, self.imgHeight))
		# self.startW, self.startH = int(round(self.imgWidth/2.0)), int(round(self.imgHeight/2.0))
		# self.player = pygame.transform.smoothscale(self.player, (self.startW, self.startH))
		self.player.set_colorkey((0,0,0))
		# self.player.fill((0, 0, 0))
		self.player.blit(self.playerImage, (0,0))
		# sets location of surface to where ever is specified
		self.rect = self.player.get_rect() 
		self.rect.centerx = x
		self.rect.centery = y

	def isColliding(self, obj):
		objRect = obj.getRect()
		return self.rect.colliderect(objRect)

	def updateRow(self, maxRows):
		if self.curRow < maxRows:
			self.curRow += 1

	def move(self, dx, dy):
		self.rect.centerx += dx
		self.rect.centery += dy
		# pygame.draw.circle(self.player, (0, 255, 0), (self.r, self.r), self.r, 0) # redraws circle

	def draw(self, surface):
		surface.blit(self.player, self.rect)

	def getRect(self): return (self.rect.centerx, self.rect.centery)