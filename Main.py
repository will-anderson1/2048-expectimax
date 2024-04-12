import WebManager
from Board import SimulatedBoard
from Search import Expectimax
import time
import json
import os
manager = WebManager.WebManager()
configFile = open("config.json")
config = json.load(configFile)
os.environ["depth"] = str(config["depth"])
os.environ["randomChanceSamplingCount"] = str(config["randomChanceSamplingCount"])
os.environ["montonicityWeight"] = str(config["montonicityWeight"])
os.environ["emptinessWeight"] = str(config["emptinessWeight"])
while True:
    board = SimulatedBoard(manager.board)
    move = Expectimax(board, int(os.environ.get("depth"))).search()
    if(move == 0):
        print("No moves left")
        print(manager.board)
        time.sleep(30)
    manager.doMove(move)

