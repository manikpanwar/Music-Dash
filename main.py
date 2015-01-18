# MHacks V project
# main game file

import pygame, sys, os
from pygame.locals import *
from animationSkeleton import AnimationSkeleton
from obstaclesAndMusicNotes import Obstacle
from obstaclesAndMusicNotes import MusicNote
from player import Player
from board import Board
from lifeMeter import LifeMeter
from musicGenerator import MusicGenerator  

class MusicDash(AnimationSkeleton):

    def __init__(self):
        super(MusicDash, self).__init__()
        self.FPS = 30

    @staticmethod
    def getIntToNoteDict():
        d = dict()
        for val in xrange(128):
            if val%12 == 0:
                d[val] ="C"
            elif val%12 == 1:
                d[val] = "C#"
            elif val%12 == 2:
                d[val] = "D"
            elif val%12 == 3:
                d[val] = "D#"
            elif val%12 == 4:
                d[val] = "E"
            elif val%12 == 5:
                d[val] = "F"
            elif val%12 == 6:
                d[val] = "F#"
            elif val%12 == 7:
                d[val] = "G"
            elif val%12 == 8:
                d[val] = "G#"
            elif val%12 == 9:
                d[val] = "A"
            elif val%12 == 10:
                d[val] = "A#"
            elif val%12 == 11:
                d[val] = "B"
        return d

    def initAnimation(self):
        self.margin = 50
        self.numNotesAtATime = 100
        self.m = MusicGenerator()
        self.trainingFilePath = "/Users/manikpanwar/Desktop/Manik/Git/Music-Dash/trainingMidiFiles/MozartCMajor"
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
        self.end = self.noteHit = False
        self.score = 0
        self.combo = 0
        self.scoreThreshold = 0
        self.intToNoteDict = MusicDash.getIntToNoteDict()
        self.meter = LifeMeter()
        pygame.display.set_caption("Music-Dash !")
        # self.backgroundImage = pygame.image.load("vanishing1.jpg")
        # self.backgroundImage.convert_alpha()
        # self.backgroundRect = self.backgroundImage.get_rect()
        self.bg = pygame.Surface(self.screen.get_size())
        self.bg.fill((66, 255, 35))

    def drawBg(self):
        screenX = self.width
        screenY = self.height
        oriX = screenX // 2
        oriY = screenY // 2
        center = (oriX, oriY)
        leftBottom = (0, screenY)
        rightBottom = (screenX, screenY)
        line_w = 2
        GREEN = (96, 96, 96)
        pygame.draw.line(self.bg, GREEN, center, leftBottom, line_w)
        pygame.draw.line(self.bg, GREEN, center, rightBottom, line_w)
        color = [(255, 102, 102),
        (255, 178, 102),
        (255, 255, 102),
        (178, 255, 102),
        (102, 255, 102),
        (102, 255, 178)]
        lenColor = len(color)
        offset = 1
        period = 16
        
        def rainbow(start, period):
            for i in range(period):
                change = i * i * offset
                change2 = (i + 1) * (i + 1) * offset
                (pygame.draw.polygon(self.bg, color[((-1)*i + start) % lenColor], 
                    ((oriX - change, oriY + change), (oriX + change, oriY + change), 
                        (oriX + change2, oriY + change2), (oriX - change2, oriX + change2))))
        rainbow(self.time, period)


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
                    self.combo += 1
                    if self.combo % 25 == 0 and self.combo != 0:
                        self.score += 50
                    if not self.musicNotes:
                        self.musicNotes = self.m.generateMusic(self.numNotesAtATime)
                    self.m.playNoteOneAtATime(self.musicNotes[0])
                    # print self.intToNoteDict[self.musicNotes[0]] # !!!
                    # self.drawNoteNames()
                    self.noteHit = True
                    self.musicNotes = self.musicNotes[1:]
                elif type(obj) == Obstacle:
                    # hit a rest 
                    self.noteHit = False
                self.meter.manageLife(obj)
                self.objectsOnScreen = self.objectsOnScreen[:i] + self.objectsOnScreen[i+1:]
            else:
                i += 1

        # Added Game Over Clause here!!
        if self.meter.checkGameOver():
            self.gameOver()

    def drawNoteNames(self):
        fontsize = 24
        font = pygame.font.Font("RobotoCondensed-Regular.ttf", fontsize)
        text = font.render("Last Note Hit: %s" % self.intToNoteDict[self.musicNotes[0]], 0, (0,0,0))
        textpos = text.get_rect()
        textpos.centerx = self.width-2*self.margin
        textpos.centery = self.margin/2.0
        self.screen.blit(text, textpos)

    def drawGameOver(self):
        fontSize = 30
        font = pygame.font.Font("RobotoCondensed-Regular.ttf", fontSize)
        text = font.render("Game Over!", 0, (0, 0, 0))
        textpos = text.get_rect()
        textpos.centerx = self.width/2.0
        textpos.centery = self.height/2.0 - self.margin
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
            if self.counter%15 == 0:
                self.drawBg()
            if self.counter%30 == 0:
                self.time += 1
                if (self.endOfBoard()):
                    self.board = Board().getBoard()
                    self.addObjects()
                else:
                    self.addObjects()
            # elif self.counter/10 > self.resizeManager:
            #   self.resizeManager += 1
            #   self.resizeObjects()
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
        font = pygame.font.Font("RobotoCondensed-Regular.ttf", fontSize)
        text = font.render("Score: %d" % self.score, 0, (0, 0, 0))
        textpos = text.get_rect()
        textpos.centerx = self.width/2.0
        textpos.centery = self.margin
        self.screen.blit(text, textpos)

    def drawBackground(self):
        self.screen.blit(self.backgroundImage, self.backgroundRect)

    def dealWithBlitting(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.bg, (0, 0))
        # self.drawBackground()
        for obj in self.objectsOnScreen:
            obj.draw(self.screen)
        self.meter.draw(self.screen)
        self.player.draw(self.screen)
        self.drawScore()
        if self.noteHit: self.drawNoteNames()
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
                self.player.move(-8, 0)
            elif keys[K_RIGHT]:
                self.player.move(8, 0)

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