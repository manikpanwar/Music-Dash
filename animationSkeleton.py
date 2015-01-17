# Animation Skeleton for pygame animations

import pygame, sys
from pygame.locals import *

# new "BasicAnimationRunner" for pygame
class AnimationSkeleton(object):

	def initAnimation(self): pass
	def onMouseDown(self, event): pass
	def onMouseMotion(self, event): pass
	def onMouseUp(self, event): pass
	def onKeyDown(self, event): pass
	def onKeyUp(self, event): pass
	def draw(self): pass
	def onTick(self): pass

	# initializes window size (width and height are optional parameters) and 
	# window itself, initializes pygame, and the frames per second
	def __init__(self, width=500, height=500):
		self.width = width
		self.height = height
		pygame.init()
		self.screen = pygame.display.set_mode((self.width, self.height), 0, 32)
		self.clock = pygame.time.Clock()
		self.FPS = 50

	def run(self):

		# initializes all the variables necessary for the animation
		self.initAnimation()

		while True:

			# handles events
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()

				elif event.type == KEYDOWN:
					self.onKeyDown(event)

				elif event.type == KEYUP:
					self.onKeyUp(event)

				elif event.type == MOUSEBUTTONDOWN:
					self.onMouseDown(event)

				elif event.type == MOUSEMOTION:
					self.onMouseMotion(event)

				elif event.type == MOUSEBUTTONUP:
					self.onMouseUp(event)

			# handles timer dependent events
			self.onTick()
			pygame.display.update()
			self.clock.tick(self.FPS)