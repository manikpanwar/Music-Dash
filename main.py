# main game file

import pygame, sys, os
from pygame.locals import *
from animationSkeleton import AnimationSkeleton

class MusicDash(AnimationSkeleton):

	def initAnimation(self):
		self.obstacle = Obstacle(self.width/2.0, self.height/2.0)

	def removeObjects(self, objects):
		for i in xrange(len(objects)):
			obj = objects[i]
			if self.isOffScreen(obj):
				objects = objects[:i] + objects[i+1:]

	def isOffScreen(self, obj):
		(x, y) = obj.getRect()
		return not((0 <= x <= self.width) or (0 <= y <= self.height))

	def onTick(self):
		if self.isOnScreen(self.obstacle):
			self.obstacle.move(1, 1)
		self.obstacle.draw(self.screen)

		
app = MusicDash()
app.run()

