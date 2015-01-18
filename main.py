# MHacks V project
# main game file

import pygame, sys, os
from pygame.locals import *
from animationSkeleton import AnimationSkeleton
from obstaclesAndMusicNotes import Obstacle, MusicNote
from player	import Player
from board import Board

class MusicDash(AnimationSkeleton):

	def __init__(self):
		super(MusicDash, self).__init__()
		self.FPS = 30

	def initAnimation(self):
		self.margin = 50
		self.board = Board().getBoard()
		self.cx, self.cy = self.width/2.0, self.height/2.0
		# self.objectsOnScreen = [Obstacle(self.width/2.0, self.height/2.0, (1, 1)), MusicNote(self.width/2.0, self.height/2.0, (-1, 1))]
		self.objectsOnScreen = []
		self.player = Player(self.width/2.0, self.height - self.margin)
		self.screen.fill((255, 255, 255))
		self.counter = 100
		self.time = 0
		self.curRow = 0
		self.cols = len(self.board[0])
		self.rows = len(self.board)
		self.velocityKey = [(-1/(3**.5), 2), (0, 2), (2/(3**.5), 2)]
		# self.velocityKey = [(-1, 1), (0, 1), (1, 1)]

	# def removeObjects(self):
	# 	temp = []
	# 	for i in xrange(len(self.objectsOnScreen)):
	# 		obj = self.objectsOnScreen[i]
	# 		if not(self.player.isColliding(obj)) or not(self.isOffScreen(obj)):
	# 			temp.append(obj)
	# 	self.objectsOnScreen = temp
	# 	# print self.objectsOnScreen

	def removeObjects(self):
		i = 0
		while (i < len(self.objectsOnScreen)):
			obj = self.objectsOnScreen[i]
			if self.isOffScreen(obj) or self.player.isColliding(obj):
				self.objectsOnScreen = self.objectsOnScreen[:i] + self.objectsOnScreen[i+1:]
			else:
				i += 1


	def isOffScreen(self, obj):
		(x, y) = obj.getLoc()
		return not((0 <= x <= self.width) or (0 <= y <= self.height))

	def moveObjects(self):
		for obstacle in self.objectsOnScreen:
			if not (self.isOffScreen(obstacle)):
				obstacle.move()

	def addObjects(self):
		for col in xrange(self.cols):
			if self.board[self.curRow][col] == "good note":
				self.objectsOnScreen.append(MusicNote(self.cx, self.cy, self.velocityKey[col]))
			elif self.board[self.curRow][col] == "obstacle":
				self.objectsOnScreen.append(Obstacle(self.cx, self.cy, self.velocityKey[col]))

			if col == 2:
				print self.velocityKey[col]
		# print self.objectsOnScreen
		self.curRow += 1

	def onTick(self):

		self.counter += 1
		if self.counter/60 > self.time:
			self.time += 1
			self.addObjects()
		self.moveObjects()
		self.removeObjects()
		self.dealWithBlitting()

	def dealWithBlitting(self):
		self.screen.fill((255, 255, 255))

		for obj in self.objectsOnScreen:
			obj.draw(self.screen)
		self.player.draw(self.screen)

	def onKeyDown(self, event): 

		if event.key == K_LEFT: 
			self.player.move(-10, 0)
		elif event.key == K_RIGHT:
			self.player.move(10, 0)

		
app = MusicDash()
app.run()

