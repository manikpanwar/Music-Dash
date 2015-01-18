# MHacks V project
# main game file

import pygame, sys, os
from pygame.locals import *
from animationSkeleton import AnimationSkeleton
from obstaclesAndMusicNotes import Obstacle
from obstaclesAndMusicNotes import MusicNote
from player	import Player
from board import Board
from lifeMeter import LifeMeter

class MusicDash(AnimationSkeleton):

	def __init__(self):
		super(MusicDash, self).__init__()
		self.FPS = 30

	def initAnimation(self):
		self.margin = 50
		self.board = Board(10).getBoard()
		self.nextBoard = Board(10).getBoard()
		self.cx, self.cy = self.width/2.0, self.height/2.0
		self.objectsOnScreen = []
		self.player = Player(self.width/2.0, self.height - self.margin)
		self.screen.fill((255, 255, 255))
		self.counter = 30
		self.time = 0
		self.resizeManager = 0
		self.curRow = 0
		self.cols = len(self.board[0])
		self.rows = len(self.board)
		self.velocityKey = [(-1/(3**.5), 2), (0, 2), (2/(3**.5), 2)]
		self.addObjects()
		self.end = False
		self.score = 0
		self.meter = LifeMeter()

	def removeObjects(self):
		i = 0
		while (i < len(self.objectsOnScreen)):
			obj = self.objectsOnScreen[i]
			if self.isOffScreen(obj): 
				self.objectsOnScreen = self.objectsOnScreen[:i] + self.objectsOnScreen[i+1:]
			elif self.player.isColliding(obj):
				if type(obj) == MusicNote:
					print "yo"
					self.score += 10
				self.meter.manageLife(obj)
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
		self.curRow = (self.curRow + 1) % 10

	def onTick(self):

		if not self.end:
			self.counter += 1
			if self.counter/30 > self.time:
				self.time += 1
				if (self.endOfBoard()):
					self.board = Board(10).getBoard()
					self.addObjects()
				else:
					self.addObjects()
			# elif self.counter/10 > self.resizeManager:
			# 	self.resizeManager += 1
			# 	self.resizeObjects()
			self.moveObjects()
			self.removeObjects()
			self.dealWithBlitting()

	def resizeObjects(self):
		for obj in self.objectsOnScreen:
			obj.resize(self.FPS)

	def endOfBoard(self):
		return self.curRow == self.rows

	def dealWithBlitting(self):
		self.screen.fill((255, 255, 255))

		for obj in self.objectsOnScreen:
			obj.draw(self.screen)
		self.meter.draw(self.screen)
		self.player.draw(self.screen)

	def onKeyDown(self, event):

		if event.key == K_p: self.end = not(self.end)
		elif event.key == K_s: 
			for obj in self.objectsOnScreen:
				obj.resize(self.FPS)

	def run(self):

		self.initAnimation()
		while True:
			# being able to hold down keys based on solution from stack overflow by qiao
			keys = pygame.key.get_pressed()
			if keys[K_LEFT]: 
				self.player.move(-5, 0)
			elif keys[K_RIGHT]:
				self.player.move(5, 0)

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

		
# app = MusicDash()
# app.run()

