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
os.environ["heuristic"] = str(config["heuristic"])
steps = 0
startTime = time.time()
while True:
    board = SimulatedBoard(manager.board)
    if(len(board.getPossibleMoveStates()) == 0 or board.getMaxTile() == 2048):
        time.sleep(2)
        print("No moves left")
        print(manager.board)
        with open('results.csv', 'a') as fd:
            score = manager.getScore()
            max = board.getMaxTile()
            print("WRITING TO RESULTS FILE")
            fd.write(str(config["heuristic"])+',' +str(time.time() - startTime)+ ',' + str(config["randomChanceSamplingCount"])+ ',' + str(config["depth"])+ ',' + str(config["montonicityWeight"])+ ',' + str(config["emptinessWeight"])+ ',' + str(score) + ',' + str(max) + ',' + str(steps) + "\n")
            steps = 0
        manager = WebManager.WebManager()
        startTime = time.time()
        continue
    move = Expectimax(board, int(os.environ.get("depth"))).search()
    manager.doMove(move)
    steps+=1

