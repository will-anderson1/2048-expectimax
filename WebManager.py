from selenium import webdriver
import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
class WebManager:
    def makeDriver(self):
        options = webdriver.ChromeOptions()
        options.add_argument(r"user-data-dir=/Users/will/Library/Application Support/Google/Chrome/Default/")
        options.add_argument(r"--profile-directory=Default")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.set_page_load_timeout(60)
        driver.get("https://play2048.co/")
        self.moveMap = {"up": Keys.ARROW_UP, "down": Keys.ARROW_DOWN, "left": Keys.ARROW_LEFT, "right": Keys.ARROW_RIGHT}
        self.driver = driver
    def updateBoard(self):
        tileContainer = self.driver.find_element(By.CLASS_NAME, "tile-container")
        tiles = tileContainer.find_elements(By.CSS_SELECTOR, "div")
        for tile in tiles:
            # class="tile tile-2 tile-position-1-1"
            # parse ints, first int as value, next int is col, last int is row
            className = tile.get_attribute("class")
            if("tile-merged" in className or "tile-inner" in className):
                continue
            ints = re.findall(r'\d+', className)
            # print(ints)
            self.board[int(ints[2]) - 1][int(ints[1]) - 1] = int(ints[0])
    def doMove(self, move):
        self.driver.find_element(By.TAG_NAME, "body").send_keys(self.moveMap[move])
        self.board = self.updateBoard()
    def play(self):
        while True:
            self.doMove("up")
            print(self.board)
            time.sleep(1)
            self.doMove("right")
            time.sleep(1)
            self.doMove("down")
            time.sleep(1)
            self.doMove("left")
            time.sleep(1)
    def __init__(self):
        self.makeDriver()
        self.board = [[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0]]
        self.updateBoard()
if __name__ == "__main__":
    manager = WebManager()
    manager.play()
