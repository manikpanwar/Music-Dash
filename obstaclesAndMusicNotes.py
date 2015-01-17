# MHacks Project
# Classes for Obstacles (rests) and MusicNotes

import pygame 

class Obstacle(object):

	def __init__(self, x, y):
		# creates surface with image of rest on it 
		self.image = pygame.image.load("rest.png") 
		self.rect = self.image.get_rect()
		(self.imgWidth, self.imgHeight) = self.rect.size
		self.obstacle = pygame.Surface((self.imgWidth*2, self.imgHeight*2))
		self.obstacle.blit(self.image, (self.rect.centerx, self.rect.centery))
		# sets location of surface to where ever is specified
		self.rect.centerx = x
		self.rect.centery = y

	def move(self, dx, dy):
		# moves surface with image on it
		self.rect.centerx += dx
		self.rect.centery += dy

	def getRect(self): return (self.rect.centerx, self.rect.centery)

	def draw(self, surface):
		# draws the local surface onto the main surface (the screen/bg) 
		surface.blit(self.obstacle, self.getRect())

class MusicNote(object):

	def __init__(self, x, y):
		self.image = pygame.image.load("rest.png") 
		self.rect = self.image.get_rect()
		(self.imgWidth, self.imgHeight) = self.rect.size
		self.musicNote = pygame.Surface((self.imgWidth*2, self.imgHeight*2))
		self.musicNote.blit(self.image, (self.rect.centerx, self.rect.centery))
		self.rect.centerx = x
		self.rect.centery = y

	def move(self, dx, dy):
		self.rect.centerx += dx
		self.rect.centery += dy

	def getRect(self): return (self.rect.centerx, self.rect.centery)

	def draw(self, surface): 
		surface.blit(self.musicNote, self.getRect())




