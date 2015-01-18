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
		# self.startW, self.startH = int(round(self.imgWidth/2.0)), int(round(self.imgHeight/2.0))
		# self.obstacle = pygame.transform.smoothscale(self.obstacle, (self.startW, self.startH))
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
		self.rect.centerx += self.dx
		self.rect.centery += self.dy

	def getRect(self): return self.rect

	def getLoc(self): 
		return (self.rect.centerx, self.rect.centery) # location

	def resize(self, FPS):
		# self.obstacle = pygame.transform.smoothscale(self.obstacle, ((int(round(self.imgWidth*ratio))), (int(round(self.imgHeight*ratio)))))
		# self.obstacle = pygame.transform.smoothscale(self.obstacle, (int(round(self.imgWidth+1.0*self.imgWidth/FPS)), int(round(self.imgHeight+1.0*self.imgHeight/FPS))))
		# self.imgWidth += 1.0*self.imgWidth/FPS
		# self.imgHeight += 1.0*self.imgHeight/FPS
		self.imgWidth *= 1.05 
		self.imgHeight *= 1.05
		# newSurface = pygame.Surface((int(round(self.imgWidth)), int(round(self.imgHeight))))
		self.obstacle = pygame.transform.smoothscale(self.obstacle, (int(round(self.imgWidth)), int(round(self.imgHeight))))

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
		# self.startW, self.startH = int(round(self.imgWidth/2.0)), int(round(self.imgHeight/2.0))
		# self.musicNote = pygame.transform.smoothscale(self.musicNote, (self.startW, self.startH))
		self.musicNote.blit(self.image, (0,0))
		self.musicNote.set_colorkey((255, 255, 255))
		self.rect.centerx = x
		self.rect.centery = y
		self.dx, self.dy = vel

	def move(self):
		self.rect.centerx += self.dx
		self.rect.centery += self.dy

	def getRect(self): return self.rect

	def resize(self, FPS):
		self.imgWidth += self.imgWidth/(2.0*FPS)
		self.imgHeight += self.imgHeight/(2.0*FPS)
		newSurface = pygame.Surface((int(round(self.imgWidth)), int(round(self.imgHeight))))
		self.musicNote = pygame.transform.smoothscale(self.musicNote, (int(round(self.imgWidth)), int(round(self.imgHeight))), newSurface)

	def getLoc(self): 
		return (self.rect.centerx, self.rect.centery) # location

	def draw(self, surface): 
		surface.blit(self.musicNote, self.getRect())





