
from Sudoku import solveSudoku
from WebHandler import WebHandler, Difficulty
from random import randint, random
from WebSudokuSolver import WebSudokuSolver
if __name__ == '__main__':
    solver = WebSudokuSolver()
    solver.handler.signIn()
    for i in range(253):
        try:
            solver.solve(Difficulty.Easy, 8 * 60 + 30 + randint(20, 80))
        except:
            continue
    # for difficulty in range(Difficulty.Hard):
    #     for i in range(50):
    #         try:
    #             solver.solve(Difficulty.Hard - difficulty, 5 * 60 + randint(20, 80))
    #         except:
    #             continue
