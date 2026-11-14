"""Sudoku puzzle generation helpers."""

import copy
import random

from sudoku import EMPTY, SIZE
from sudoku.solver import fill_board


def deep_copy(board: list[list[int]]) -> list[list[int]]:
    """Return a deep copy of a Sudoku board."""
    return copy.deepcopy(board)


def create_empty_board() -> list[list[int]]:
    """Return a new 9-by-9 board containing only empty cells."""
    return [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]


def remove_cells(board: list[list[int]], clues: int) -> None:
    """Remove cells from a solved board until the requested clue count remains."""
    cells_to_remove = SIZE * SIZE - clues
    while cells_to_remove > 0:
        row = random.randrange(SIZE)
        col = random.randrange(SIZE)
        if board[row][col] != EMPTY:
            board[row][col] = EMPTY
            cells_to_remove -= 1


def generate_puzzle(clues: int = 35) -> tuple[list[list[int]], list[list[int]]]:
    """Generate and return a puzzle board and its completed solution."""
    if not 0 <= clues <= SIZE * SIZE:
        raise ValueError("Clues must be an integer between 0 and 81")

    solution = create_empty_board()
    fill_board(solution)
    puzzle = deep_copy(solution)
    remove_cells(puzzle, clues)
    return puzzle, solution
