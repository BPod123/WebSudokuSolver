from Sudoku import solveSudoku
from WebHandler import WebHandler, Difficulty
from time import sleep, time
class WebSudokuSolver(object):
    def __init__(self):
        self.handler = WebHandler()
    def solve(self, difficulty:Difficulty, timeTaken):
        # if self.handler.difficulty != difficulty:
            # self.handler.signIn()
        self.handler.selectDifficulty(difficulty)
        # waitBegin = time()
        # while len(self.handler.driver.find_elements_by_id("f00")) == 0 and (time() - waitBegin) < 10:
        #     pass

        start = time()
        puzzle = self.handler.newPuzzle()
        solved, soln = solveSudoku(puzzle)
        end = time()
        inputTime = abs(timeTaken - (end - start))
        self.handler.inputSolution(soln, inputTime)
        self.handler.submit()
        sleep(10)
        self.handler.reset()
