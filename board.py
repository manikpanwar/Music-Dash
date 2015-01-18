# Board Class for the runner game Music-Dash

import pygame
import random
from animationSkeleton import AnimationSkeleton

class Board(object):
    @staticmethod
    def make2dList(rows, cols):
        ls = []
        for row in xrange(rows):
            ls += [["empty"]*cols]
        return ls

    @staticmethod
    def maxItemLength(a):
        # from 112 class website
        maxLen = 0
        rows = len(a)
        cols = len(a[0])
        for row in xrange(rows):
            for col in xrange(cols):
                maxLen = max(maxLen, len(str(a[row][col])))
        return maxLen

    @staticmethod
    def print2dList(a):
        # from 112 class website
        if (a == []):
            # So we don't crash accessing a[0]
            print []
            return
        rows = len(a)
        cols = len(a[0])
        fieldWidth = Board.maxItemLength(a)
        print "[ ",
        for row in xrange(rows):
            if (row > 0): print "\n  ",
            print "[ ",
            for col in xrange(cols):
                if (col > 0): print ",",
                # The next 2 lines print a[row][col] with the given fieldWidth
                format = "%" + str(fieldWidth) + "s"
                print format % str(a[row][col]),
            print "]",
        print "]"

    def makeBoardEmpty(self):
        for row in xrange(self.rows):
            for col in xrange(self.cols):
                self.board[row][col] = "empty"

    def reInitGameBoard(self):
        # function which can be called when we have rendered all the rows in the board 
        # to randomly generate a new board, thereby extending it to
        # infinite length
        self.makeBoardEmpty()
        self.fillObstaclesInBoard()
        self.fillGoodMusicNotesInBoard()

    def colIsValidForNote(self, col1, col2):
        return abs(col1 - col2) <= 1

    def fillObstaclesInBoard(self):
        board = self.board
        rows, cols = self.rows, self.cols
        obstacleColumnsInPrevRow = []
        board[0][0] = "obstacle"
        for row in xrange(1, rows):
            # weighting heavily for at least one obstacle
            numObstaclesInRow = random.choice([0, 1, 1, 2])
            cols = [0, 1, 2]
            # print numObstaclesInRow
            if numObstaclesInRow == 1:
                for col in cols:
                    if col not in obstacleColumnsInPrevRow:
                        obstacleColumnsInPrevRow = [col]
                        break
                board[row][col] = "obstacle"
            elif numObstaclesInRow == 2:
                col1 = col2 = -1
                while(col1 == col2):
                    col1, col2 = random.choice([0, 1, 2]), random.choice([0, 1, 2])
                board[row][col1] = "obstacle"
                board[row][col2] = "obstacle"
            else:
                # no obstacles
                continue

    def fillGoodMusicNotesInBoard(self):
        # puts in music notes in the board in such a way that there is 
        # always a path that the player can take to get all the music notes 
        # and reach till the numRows'th row which is at index 49
        # goal: reaching row index (numRows - 1) is a successful path

        # the way I have set up the obstacles it is now possible to lay the
        # good music notes greedily and still meet the goal. this will make 
        # runtime fast and eliminate the need for breadth first search

        #@TODO: Could try out different ways of laying obstacles
        board = self.board
        rows, cols = self.rows, self.cols
        prevNoteCol = 0
        for row in xrange(1, rows):
            c = [0, 1, 2]
            random.shuffle(c)
            # print c
            for col in c:
                # make sure good notes are well distributed
                if (board[row][col] == "empty" and 
                                    self.colIsValidForNote(prevNoteCol, col)):
                    self.board[row][col] = "good note"
                    prevNoteCol = col
                    break


    def fillBoard(self):
        self.fillObstaclesInBoard()
        self.fillGoodMusicNotesInBoard()
        # Board.print2dList(self.board)

    def numRows(self): return self.rows

    def numCols(self): return self.cols

    def getBoard(self): return self.board

    def __init__(self, rows = 50, columns = 3):
        self.rows, self.cols = rows, columns
        self.board = Board.make2dList(rows, columns)
        self.fillBoard()

        # self.curRow = 0 # current row of the player indexed from zero for convenience
        # self.playerTimeTakenToCoverOneRow = 2 # seconds
        # self.playerSpeed = 1.0/ self.playerTimeTakenToCoverOneRow
