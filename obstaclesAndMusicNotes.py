# MHacks Project
# Classes for Obstacles (rests) and MusicNotes

import pygame 

class Obstacle(object):

	def __init__(self, x, y, vel):
		# creates surface with image of rest on it 
		self.image = pygame.image.load("rest.png") 
		self.image.convert_alpha()
		self.imageRect = self.image.get_rect()
		(self.imgWidth, self.imgHeight) = self.imageRect.size
		self.obstacle = pygame.Surface((self.imgWidth, self.imgHeight))
		self.obstacle.set_colorkey((255,255,255))
		# self.obstacle.fill((0, 0, 0))
		self.obstacle.blit(self.image, (0,0))
		# sets location of surface to where ever is specified
		self.rect = self.obstacle.get_rect() 
		self.rect.centerx = x
		self.rect.centery = y
		(self.dx, self.dy) = vel

	def move(self):
		# moves surface with image on it
		print "vel", self.dx, self.dy
		self.rect.centerx += self.dx
		self.rect.centery += self.dy
		print self.rect.centerx, self.rect.centery

	def getRect(self): return self.rect

	def getLoc(self): 
		return (self.rect.centerx, self.rect.centery) # location

	def draw(self, surface):
		# draws the local surface onto the main surface (the screen/bg) 
		surface.blit(self.obstacle, self.getLoc())

class MusicNote(object):

	def __init__(self, x, y, vel):
		self.image = pygame.image.load("eighthNote.png") 
		self.image.convert_alpha()
		self.rect = self.image.get_rect()
		(self.imgWidth, self.imgHeight) = self.rect.size
		self.musicNote = pygame.Surface((self.imgWidth, self.imgHeight))
		self.musicNote.blit(self.image, (0,0))
		self.musicNote.set_colorkey((255, 255, 255))
		self.rect.centerx = x
		self.rect.centery = y
		self.dx, self.dy = vel

	def move(self):
		print "vel", self.dx, self.dy
		self.rect.centerx += self.dx
		self.rect.centery += self.dy
		print self.rect.centerx, self.rect.centery

	def getRect(self): return self.rect

	def getLoc(self): 
		return (self.rect.centerx, self.rect.centery) # location

	def draw(self, surface): 
		surface.blit(self.musicNote, self.getRect())





