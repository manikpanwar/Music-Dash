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
from musicGenerator import MusicGenerator  

class MusicDash(AnimationSkeleton):

	def __init__(self):
		super(MusicDash, self).__init__()
		self.FPS = 30

	def initAnimation(self):
		self.margin = 50
		self.numNotesAtATime = 100
		self.m = MusicGenerator()
		self.trainingFilePath = "/Users/manikpanwar/Desktop/Manik/Git/Music-Dash/trainingMidiFiles/bartok"
		self.m.train(self.trainingFilePath)
		self.musicNotes = self.m.generateMusic(self.numNotesAtATime)
		self.board = Board().getBoard()
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
		self.scoreThreshold = 0
		self.meter = LifeMeter()
		pygame.display.set_caption("Music-Dash !")
		self.backgroundImage = pygame.image.load("vanishing1.jpg")
		self.backgroundImage.convert_alpha()
		self.backgroundRect = self.backgroundImage.get_rect()

	def increaseVel(self, dx, dy):
		if dx < 0: 
			dx = max(dx - 1, -1/(3**.5)-5)
		elif dx >0: 
			dx = min(dx+1, (2/(3**.5))+5) 
		dy = min(dy+1, 7) 
		return (dx, dy)

	def keepScore(self):
		self.score += 10
		temp = []
		if self.score/200 > self.scoreThreshold:
			self.scoreThreshold += 1
			for dx, dy in self.velocityKey:
				temp.append(self.increaseVel(dx, dy))
			self.velocityKey = temp

	def removeObjects(self):
		i = 0
		while (i < len(self.objectsOnScreen)):
			obj = self.objectsOnScreen[i]
			if self.isOffScreen(obj): 
				if type(obj) == MusicNote:
					self.meter.manageLife()
				self.objectsOnScreen = self.objectsOnScreen[:i] + self.objectsOnScreen[i+1:]
			elif self.player.isColliding(obj):
				if type(obj) == MusicNote:
					self.keepScore()
					if not self.musicNotes:
						self.musicNotes = self.m.generateMusic(self.numNotesAtATime)
					self.m.playNoteOneAtATime(self.musicNotes[0])
					self.musicNotes = self.musicNotes[1:]
				self.meter.manageLife(obj)
				self.objectsOnScreen = self.objectsOnScreen[:i] + self.objectsOnScreen[i+1:]
			else:
				i += 1

		# Added Game Over Clause here!!
		if self.meter.checkGameOver():
			self.gameOver()

	def drawGameOver(self):
		fontSize = 30
		font = pygame.font.Font(None, fontSize)
		text = font.render("Game Over!", 0, (0, 0, 0))
		textpos = text.get_rect()
		textpos.centerx = self.width/2.0
		textpos.centery = self.height/2.0
		self.screen.blit(text, textpos)

	def gameOver(self):
		self.end = True
		print "Game over"
		self.board = []
		self.objectsOnScreen = []
		self.drawGameOver()

	def isOffScreen(self, obj):
		(x, y) = obj.getLoc()
		return y >= 525

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
		self.curRow = (self.curRow + 1) % self.rows

	def onTick(self):

		if not self.end:
			self.counter += 1
			if self.counter/30 > self.time:
				self.time += 1
				if (self.endOfBoard()):
					self.board = Board().getBoard()
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

	def drawScore(self):
		fontSize = 24
		font = pygame.font.Font(None, fontSize)
		text = font.render("Score: %d" % self.score, 0, (0, 0, 0))
		textpos = text.get_rect()
		textpos.centerx = self.width/2.0
		textpos.centery = self.margin
		self.screen.blit(text, textpos)

	def drawBackground(self):
		self.screen.blit(self.backgroundImage, self.backgroundRect)

	def dealWithBlitting(self):
		self.screen.fill((255, 255, 255))
		self.drawBackground()
		for obj in self.objectsOnScreen:
			obj.draw(self.screen)
		self.meter.draw(self.screen)
		self.player.draw(self.screen)
		self.drawScore()
		if self.end: self.drawGameOver()

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