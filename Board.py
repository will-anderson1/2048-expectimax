import copy
import os
import math
import numpy as np
sArr = [
    [2**1, 2**2, 2**3, 2**4],
    [2**8, 2**7, 2**6, 2**5],
    [2**9,2**10,2**11,2**12],
    [2**16, 2**15, 2**14, 2**13]]
class SimulatedBoard:
    # takes in board, has operations like getPossibleRandomTileSpawnStates, getPossibleMoveStates
    def __init__(self, board):
        self.board = board
    def getMaxTile(self):
        return np.max(self.board)
    def getRandomChanceSample(self):
        numSamples = int(os.environ.get("randomChanceSamplingCount"))
        # .9 chance of 2, .1 chance of 4
        emptyTiles = []
        for i in range(4):
            for j in range(4):
                if(self.board[i][j] == 0):
                    emptyTiles.append((i, j))
        setOfPossibleIndices = set([x for x in range(len(emptyTiles))])
        states = []
        count = 0
        while(count < numSamples and len(emptyTiles) > 0):
            if(len(setOfPossibleIndices) == 0):
                break
            index = np.random.choice(list(setOfPossibleIndices))
            setOfPossibleIndices.remove(index)
            (i, j) = emptyTiles[index]
            newBoard = copy.deepcopy(self.board)
            if(np.random.rand() < .9):
                newBoard[i][j] = 2
            else:
                newBoard[i][j] = 4
            states.append(SimulatedBoard(newBoard))
            count += 1
        return states
    def getPossibleMoveStates(self):
        slideLeft = SimulatedBoard.slideLeft(self.board)
        slideRight = SimulatedBoard.slideRight(self.board)
        slideUp = SimulatedBoard.slideUp(self.board)
        slideDown = SimulatedBoard.slideDown(self.board)
        moveMap = {}
        if not (slideLeft is None):
            moveMap["L"] = SimulatedBoard(slideLeft)
        if not (slideRight is None):
            moveMap["R"] = SimulatedBoard(slideRight)
        if not (slideUp is None):
            moveMap["U"] = SimulatedBoard(slideUp)
        if not (slideDown is None):
            moveMap["D"] = SimulatedBoard(slideDown)
        return moveMap
    def defaultEvaluate(self):
        # test heuristic, just all empty tiles
        # add prioritizing monotonicity to top right corner
        monotonicRows = set([0,1,2,3])
        monotonicCols = set([0,1,2,3])
        count = 0
        maxNum = 0
        for i in range(4):
            for j in range(4):
                maxNum = max(maxNum, self.board[i][j])
                if self.board[i][j] == 0:
                    count += 1
                if j > 0:
                    if not (self.board[i][j] >= self.board[i][j - 1] or self.board[i][j] == 0) and j in monotonicCols:
                        monotonicCols.remove(j)
                    if not (self.board[j][i] >= self.board[j - 1][i] and self.board[j][i] != 0) and j in monotonicRows:
                        monotonicRows.remove(j)
        monontonicityScore = 0
        for i in monotonicCols:
            monontonicityScore += i
        for i in monotonicRows:
            monontonicityScore += i
        if(self.board[3][3] == maxNum):
            monontonicityScore += 2
        if(count == 0):
            return 0
        else:
            if self.getMaxTile() == 2048:
                return math.inf 
            return (float(os.environ.get("emptinessWeight")) * count) + (float(os.environ.get("montonicityWeight")) * monontonicityScore)
    
    def sEvaluate(self):
        count = 0
        heuristic = 0
        for i in range(4):
            for j in range(4):
                heuristic += sArr[i][j] * self.board[i][j]
                if self.board[i][j] == 0:
                    count += 1
                
        if(count == 0):
            return 0
        else:
            return heuristic
    def evaluate(self):
        if(os.environ.get("heuristic") == "sHeuristic"):
            return self.sEvaluate()
        else:
            return self.defaultEvaluate()
    def slideLeft(board):
        newBoard = copy.deepcopy(board)
        moved = False
        for rowIndex in range(4):
            row = [x for x in newBoard[rowIndex] if x != 0]
            newRow = []
            while(len(row) > 0):
                if(len(row) == 1):
                    newRow.append(row.pop(0))
                else:
                    element = row.pop(0)
                    if(row[0] == element):
                        row.pop(0)
                        newRow.append(element * 2)
                    else:
                        newRow.append(element)
            for i in range(0, 4 - len(newRow)):
                newRow.append(0)
            if(not (np.array_equal(newRow, newBoard[rowIndex]))):
                moved = True
            newBoard[rowIndex] = newRow
        if(moved):
            return newBoard
        return None
    def slideRight(board):
        newBoard = copy.deepcopy(board)
        moved = False
        for rowIndex in range(4):
            
            row = [x for x in newBoard[rowIndex] if x != 0]
            newRow = []
            while(len(row) > 0):
                if(len(row) == 1):
                    newRow = [row.pop()] + newRow
                else:
                    element = row.pop()
                    if(row[len(row) - 1] == element):
                        row.pop()
                        newRow = [element*2] + newRow
                    else:
                        newRow = [element] + newRow
            padding = []
            for i in range(0, 4 - len(newRow)):
                padding.append(0)
            padding = padding + newRow
            if(not (np.array_equal(padding, newBoard[rowIndex]))):
                moved = True
            newBoard[rowIndex] = padding
        if(moved):
            return newBoard
        return None
    def slideUp(board):
        result = SimulatedBoard.slideLeft(np.transpose(board))
        if not (result is None):
            return np.transpose(result)
        return None
    def slideDown(board):
        rotatedBoard = np.rot90(board, 1)
        result = SimulatedBoard.slideRight(rotatedBoard)
        if not (result is None):
            return np.rot90(result, 3)
        return None
    # def slideUp(board):
    #     board = np.array(board)
    #     newBoard = np.zeros_like(board)
    #     moved = False

    #     for colIndex in range(4):
    #         column = [x for x in board[:, colIndex] if x != 0]
    #         newColumn = []
    #         while len(column) > 0:
    #             if len(column) == 1:
    #                 newColumn.append(column.pop(0))
    #             else:
    #                 element = column.pop(0)
    #                 if column[0] == element:
    #                     column.pop(0)
    #                     newColumn.append(element * 2)
    #                 else:
    #                     newColumn.append(element)
    #         newColumn += [0] * (4 - len(newColumn))
    #         if not np.array_equal(newColumn, board[:, colIndex]):
    #             moved = True
    #         newBoard[:, colIndex] = newColumn
        
    #     if moved:
    #         return newBoard
    #     return None

    # def slideDown(board):
    #     board = np.array(board)
    #     newBoard = np.zeros_like(board)
    #     moved = False

    #     for colIndex in range(4):
    #         column = [x for x in board[:, colIndex] if x != 0]
    #         newColumn = []
    #         while len(column) > 0:
    #             if len(column) == 1:
    #                 newColumn = [column.pop()] + newColumn
    #             else:
    #                 element = column.pop()
    #                 if len(column) > 0 and column[-1] == element:
    #                     column.pop()
    #                     newColumn = [element * 2] + newColumn
    #                 else:
    #                     newColumn = [element] + newColumn
    #         padding = [0] * (4 - len(newColumn))
    #         newColumn = padding + newColumn
    #         if not np.array_equal(newColumn, board[:, colIndex]):
    #             moved = True
    #         newBoard[:, colIndex] = newColumn
        
    #     if moved:
    #         return newBoard
    #     return None
