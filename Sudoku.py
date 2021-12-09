import numpy as np
from collections import defaultdict
import multiprocessing as mp
from threading import Thread


class SudokuPuzzle(np.ndarray):
    def __hash__(self):
        return tuple([x for x in self.reshape((self.size,))]).__hash__()

    def sortKey(self, space):
        spOptions = len(self.spaceOptions(space))
        nmOptions = [self.numberOptions(x) for x in self.spaceOptions(space)]
        nmOptions.sort()
        tup = tuple([spOptions] + nmOptions)
        return tup

    @property
    def potentialMoves(self):
        options = []
        for space in self.emptySpaces:
            for option in self.spaceOptions(space):
                cpy = self.copy()
                cpy[space] = option
                options.append(cpy)
        return options

    def spaceOptions(self, space):
        if not hasattr(self, '_spaceOptions'):
            self._spaceOptions = defaultdict(set)
        options = set(range(1, 10))
        # Check row and columns
        row = {self[space[0], i] for i in range(9) if i != space[1]}
        col = {self[i, space[1]] for i in range(9) if i != space[0]}
        options.difference_update(row)
        options.difference_update(col)
        if len(options) > 0:
            # Check block
            block = self[(space[0] // 3) * 3: (space[0] // 3) * 3 + 3, (space[1] // 3) * 3: (space[1] // 3) * 3 + 3]
            block = block.reshape((block.size,))
            options.difference_update(set(block))
        self._spaceOptions[space] = options
        return options

    def numberOptions(self, number: int):
        return int(sum([1 if number in self.spaceOptions(space) else 0 for space in self.emptySpaces]))

    def __setitem__(self, key, value):
        if hasattr(self, "_spaceOptions"):
            self._spaceOptions.clear()
        return super().__setitem__(key, value)

    @property
    def valid(self):
        # Check Rows
        counts = np.zeros((9, 9))
        for r in range(9):

            for c in range(9):
                if self[r, c] != -1:
                    counts[r, self[r, c] - 1] += 1
        del r, c
        if np.max(counts) > 1:
            # self._valid = False
            return False
        del counts

        counts = np.zeros((9, 9))
        # Check Columns
        for c in range(9):

            for r in range(9):
                if self[r, c] != -1:  # not np.isnan(self[r, c]):
                    counts[self[r, c] - 1, c] += 1
        del r, c
        if np.max(counts) > 1:
            # self._valid = False
            return False

        # Check Blocks
        for x in range(3):
            for y in range(3):
                del counts
                counts = np.zeros((9,))
                block = self[3 * x: 3 * x + 3, 3 * y: 3 * y + 3]
                for i in range(3):
                    for j in range(3):
                        if block[i, j] != -1:  # not np.isnan(block[i, j]):
                            counts[block[i, j] - 1] += 1
                del i, j, block
                if np.max(counts) == 2:
                    # self._valid = False
                    return False
        del x, y
        # self._valid = True
        return True

    @property
    def emptySpaces(self):
        emptyIndices = np.arange(81).reshape((9, 9))[self.view(np.ndarray) == -1]
        return [index(i) for i in emptyIndices]

    @property
    def solved(self):
        return self.valid and -1 not in self


def index(i: int):
    return i // 9, i % 9


def solveSudoku(puzzle: SudokuPuzzle):
    # g = SudokuGraph(puzzle)
    # coloring = nx.greedy_color(g)
    cpy = puzzle.copy().view(SudokuPuzzle)
    emptySpaces = cpy.emptySpaces
    if len(emptySpaces) == 0 and cpy.valid:
        return True, cpy
    minSpace = min(emptySpaces, key=lambda x: len(cpy.spaceOptions(x)))
    if len(cpy.spaceOptions(minSpace)) == 0:
        return False, None
    else:
        options = list(cpy.spaceOptions(minSpace))
        options.sort(key=lambda x: cpy.numberOptions(x))
        for option in options:  # cpy.spaceOptions(minSpace):
            cpy[minSpace] = option
            solved, soln = solveSudoku(cpy)
            if solved:
                return True, soln
        return False, None


# def processSetQueue(q: mp.Queue, s: set, solnFound: list):
#     while not solnFound[0]:
#         if q.not_empty:
#             puzzle = q.get()
#             if puzzle.solved:
#                 solnFound[0] = True
#                 return puzzle
#             s.add(puzzle)
#             q.task_done()


def findMoves(puzzle: SudokuPuzzle):
    # visited.put(puzzle)
    if puzzle.solved:
        return [], puzzle
    else:
        # moves = [x for x in puzzle.potentialMoves if x not in visited]
        return puzzle.potentialMoves, None


def multiprocessingSolve(puzzle: np.ndarray):
    sPuzzle = puzzle.view(SudokuPuzzle)
    moves = sPuzzle.potentialMoves
    # q = mp.Queue()
    pool = mp.Pool()
    visited = set()
    while True:
        for move in moves:
            visited.add(move)
        futureMoves = [pool.apply_async(findMoves, args=(move,)) for move in moves]
        moves.clear()
        results = [x.get() for x in futureMoves]
        for newMoves, soln in results:
            if newMoves == [] and soln is not None:
                pool.close()
                return soln
            else:
                for newMove in newMoves:
                    if newMove not in visited:
                        moves.append(newMove)

        # def cudaSolve(puzzle)
