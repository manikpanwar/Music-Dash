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



    def colIsValidForNote(self, col1, col2):
        return abs(col1 - col2) <= 1

    def fillObstaclesInBoard(self):
        board = self.board
        rows, cols = self.rows, self.columns
        self.fillObstaclesInBoard()
        obstacleColumnsInPrevRow = []
        for row in xrange(1, rows):
            # weighting heavily for at least one obstacle
            numObstaclesInRow = random.choice([0, 1, 1, 2])
            cols = [1 , 2, 3]
            print numObstaclesInRow
            if numObstaclesInRow == 1:
                for col in cols:
                    if col not in obstacleColumnsInPrevRow:
                        obstacleColumnsInPrevRow = [col]
                        break
                board[row][col] = "obstacle"
            elif numObstaclesInRow == 2:
                col1 = col2 = -1
                while(col1 == col2):
                    col1, col2 = random.choice([1, 2, 3]), random.choice([1, 2, 3])
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
            for col in xrange(cols):
                if board[row][col] == "empty" and 
                    self.colIsValidForNote(prevNoteCol, col):
                    self.board[row][col] = "good note"
                    break


    def fillBoard(self):
        self.fillObstaclesInBoard()
        self.fillGoodMusicNotesInBoard()

    def __init__(self, rows = 50, columns = 3):
        self.rows, self.cols = rows, columns
        self.board = Board.make2dList(rows, columns)
        self.fillBoard()
        
        # self.curRow = 0 # current row of the player indexed from zero for convenience
        # self.playerTimeTakenToCoverOneRow = 2 # seconds
        # self.playerSpeed = 1.0/ self.playerTimeTakenToCoverOneRow

