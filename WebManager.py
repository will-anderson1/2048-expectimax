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
        self.moveMap = {"U": Keys.ARROW_UP, "D": Keys.ARROW_DOWN, "L": Keys.ARROW_LEFT, "R": Keys.ARROW_RIGHT}
        self.driver = driver
    def updateBoard(self):
        time.sleep(0.2)
        # tileContainer = self.driver.find_element(By.CLASS_NAME, "tile-container")
        tiles = self.driver.find_elements(By.XPATH, '//div[@class="tile-container"]/div')
        self.board = [[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0]]
        # tile tile-4 tile-position-1-3 tile-merged
        # tile tile-2 tile-position-1-4 tile-new
        for tile in tiles:

            # class="tile tile-2 tile-position-1-1"
            # parse ints, first int as value, next int is col, last int is row
            className = tile.get_attribute("class")
            ints = re.findall(r'\d+', className)
            # print(ints)
            self.board[int(ints[2]) - 1][int(ints[1]) - 1] = int(ints[0])
    def doMove(self, move):
        self.driver.find_element(By.TAG_NAME, "body").send_keys(self.moveMap[move])
        self.updateBoard()
    def __init__(self):
        self.makeDriver()
        time.sleep(0.2)
        self.board = [[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0]]
        self.updateBoard()