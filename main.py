# MHacks V project
# main game file

import pygame, sys, os
from pygame.locals import *
from animationSkeleton import AnimationSkeleton
from obstaclesAndMusicNotes import Obstacle, MusicNote
from player	import Player
from board import Board

class MusicDash(AnimationSkeleton):

	def initAnimation(self):
		self.margin = 50
		self.board = Board()
		self.obstacles = [Obstacle(self.width/2.0, self.height/2.0, 1, 1)]
		self.player = Player(self.width/2.0, self.height - self.margin)
		self.screen.fill((255, 255, 255))

	def removeObjects(self):
		for i in xrange(len(self.obstacles)):
			obj = self.obstacles[i]
			if self.isOffScreen(obj) or self.player.isColliding(obj):
				self.obstacles = self.obstacles[:i] + self.obstacles[i+1:]

	def isOffScreen(self, obj):
		(x, y) = obj.getLoc()
		return not((0 <= x <= self.width) or (0 <= y <= self.height))

	def moveObjects(self):
		for obstacle in self.obstacles:
			if not (self.isOffScreen(obstacle)):
				obstacle.move()

	def onTick(self):

		self.moveObjects()
		self.removeObjects()
		self.dealWithBlitting()

	def dealWithBlitting(self):
		self.screen.fill((255, 255, 255))

		for obstacle in self.obstacles:
			obstacle.draw(self.screen)
		self.player.draw(self.screen)

	def onKeyDown(self, event): 

		if event.key == K_LEFT: 
			self.player.move(-10, 0)
		elif event.key == K_RIGHT:
			self.player.move(10, 0)

		
app = MusicDash()
app.run()

