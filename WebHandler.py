from selenium.webdriver import Firefox
import os
import numpy as np
from Sudoku import SudokuPuzzle
from enum import IntEnum
from time import sleep, time
from random import random

class Difficulty(IntEnum):
    Easy = 1
    Medium = 2
    Hard = 3
    Evil = 4


# from webdriver_manager.firefox import GeckoDriverManager
class WebHandler(object):
    def __init__(self):
        self.driver = Firefox(os.getcwd())
        self.puzzle = None
        self.soln = None
        self.difficulty = Difficulty.Easy
        self.signedIn = False

    def getCell(self, i, j):
        # return self.driver.find_element_by_id("c{0}{1}".format(i, j)).find_elements_by_xpath("./input")[0]
        return self.driver.find_element_by_id("f{0}{1}".format(i, j))

    def getCellValue(self, i, j):
        return self.getCell(i, j).get_attribute("value")

    def setCellValue(self, i, j, value):
        cell = self.getCell(i, j)
        cell.click()
        cell.send_keys(str(value))
        # cell.setAttribute("value", value)

    def signIn(self):
        # self.driver.get("https://grid.websudoku.com/")
        self.signedIn = True
        self.driver.get("https://nine.websudoku.com/?signin")
        sleep(2)
        email = self.driver.find_element_by_name("email")
        email.click()
        from credentials import Email, Password
        email.send_keys(Email)
        password = self.driver.find_element_by_name("password")
        password.click()
        password.send_keys(Password)
        # self.driver.find_element_by_name("remember").click()
        self.driver.find_element_by_name("do_signin").click()
        sleep(1)

    def selectDifficulty(self, difficulty: Difficulty):
        self.difficulty = difficulty
        if "level={0}".format(difficulty) not in self.driver.current_url:
            self.driver.get("https://nine.websudoku.com/?level={0}".format(difficulty))
            sleep(1)

    def newPuzzle(self):
        self.startTime = time()
        puzzle = np.zeros((9, 9), dtype=np.int)
        for i in range(9):
            for j in range(9):
                value = self.getCellValue(i, j)
                puzzle[i, j] = -1 if len(value) == 0 else int(value)
        self.puzzle = puzzle.view(SudokuPuzzle)
        return puzzle

    def inputSolution(self, soln, timeEntering):
        self.soln = soln
        # if timeEntering - time() > 6 * 60:
        #     sleep(timeEntering - 6 * 60)
        #     timeEntering -= timeEntering - 6 * 60

        spaces = self.puzzle.emptySpaces
        spaces.sort(key = lambda x: self.puzzle.sortKey(x))
        for space in spaces:
            # Enter Solution onto page
            cell = self.driver.find_element_by_id("f{0}{1}".format(space[0], space[1]))
            cell.click()
            cell.send_keys(str(soln[space]))
            # sleep(random())
            # sleep(1 / (len(spaces)  * 10) * timeEntering)
            # sleep(1/81)
            sleep(timeEntering / len(spaces))
        while time() - self.startTime < timeEntering:
            pass

    def submit(self):
        self.driver.find_element_by_name('submit').click()
        sleep(0.5)

    def reset(self):
        try:
            self.driver.find_element_by_name('newgame').click()
        except:
            if self.signedIn:
                self.signIn()
            self.selectDifficulty(self.difficulty)
        sleep(0.5)
