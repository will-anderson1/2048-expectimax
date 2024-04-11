import copy
import numpy as np
class SimulatedBoard:
    # takes in board, has operations like getPossibleRandomTileSpawnStates, getPossibleMoveStates
    def __init__(self, board):
        self.board = board
    def getRandomChanceSamplePossibleRandomTileSpawnStates(self, numSamples):
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
    def evaluate(self):
        # test heuristic, just all empty tiles
        count = 0
        for i in range(4):
            for j in range(4):
                if self.board[i][j] == 0:
                    count += 1
        return count
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
    