import WebManager
from Board import SimulatedBoard
from Search import Expectimax
import time
manager = WebManager.WebManager()
while True:
    board = SimulatedBoard(manager.board)
    move = Expectimax(board, 6).search()
    if(move == 0):
        print("No moves left")
        print(manager.board)
        time.sleep(30)
    manager.doMove(move)

