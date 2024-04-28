from Board import SimulatedBoard
import numpy as np
class Expectimax:
    # if depth is odd, this is a chance node. If depth is even, this is a max node
    def __init__(self, board, depth):
        self.depth = depth
        self.board = board
    # take MAX of result of searching left, right, up, down states.  take average of all possible random tile spawns, who have values of max of searching their left, right, up, down
    def expectimax(self, board, currentDepth):
        if currentDepth == self.depth:
            return board.evaluate()
        if currentDepth % 2 == 0:
            # check u, r, l, d, take max
            moves = board.getPossibleMoveStates()
            if len(moves) == 0:
                return board.evaluate()
            maxVal = 0;
            maxChar = ""
            # if current depth is zero, we want to return the char (l, r, u, d) of the move that is the best
            # else, we want to return the value of the best move
            if(len(moves) == 0):
                return 0
            for move in moves:
                if currentDepth == 0:
                    val = self.expectimax(moves[move], currentDepth + 1)
                    if val >= maxVal:
                        maxVal = val
                        maxChar = move
                else:
                    val = self.expectimax(moves[move], currentDepth + 1)
                    if val >= maxVal:
                        maxVal = val
            if currentDepth == 0:
                return maxChar
            return maxVal
        else:
            randomTileSpawns = board.getRandomChanceSample()
            sum = 0
            count = 0
            for state in randomTileSpawns:
                sum += self.expectimax(state, currentDepth + 1)
                count += 1
            
            return sum / count
    def search(self):
        return self.expectimax(self.board, 0)