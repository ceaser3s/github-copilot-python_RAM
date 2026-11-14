"""Sudoku puzzle generation helpers."""

import copy
import random

from sudoku import EMPTY, SIZE
from sudoku.solver import count_solutions, fill_board

DIFFICULTY_CLUES = {"easy": 42, "medium": 34, "hard": 28}


def deep_copy(board: list[list[int]]) -> list[list[int]]:
    """Return a deep copy of a Sudoku board."""
    return copy.deepcopy(board)


def create_empty_board() -> list[list[int]]:
    """Return a new 9-by-9 board containing only empty cells."""
    return [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]


def remove_cells(board: list[list[int]], clues: int) -> None:
    """Remove randomized cells while preserving a unique solution."""
    if not 0 <= clues <= SIZE * SIZE:
        raise ValueError("Clues must be an integer between 0 and 81")

    cells = [(row, col) for row in range(SIZE) for col in range(SIZE)]
    random.shuffle(cells)
    remaining = sum(value != EMPTY for row in board for value in row)

    for row, col in cells:
        if remaining <= clues:
            break
        value = board[row][col]
        if value != EMPTY:
            board[row][col] = EMPTY
            if count_solutions(board) == 1:
                remaining -= 1
            else:
                board[row][col] = value


def generate_puzzle(
    difficulty: str | int = "medium", *, clues: int | None = None
) -> tuple[list[list[int]], list[list[int]]]:
    """Generate a unique puzzle for a difficulty or legacy clue count.

    Integer positional values and the ``clues`` keyword remain supported for
    callers that used the previous clue-count API.
    """
    if clues is not None:
        target_clues = clues
    elif isinstance(difficulty, int):
        target_clues = difficulty
    elif difficulty in DIFFICULTY_CLUES:
        target_clues = DIFFICULTY_CLUES[difficulty]
    else:
        raise ValueError("Difficulty must be one of: easy, medium, hard")

    if not 0 <= target_clues <= SIZE * SIZE:
        raise ValueError("Clues must be an integer between 0 and 81")

    solution = create_empty_board()
    fill_board(solution)
    puzzle = deep_copy(solution)
    remove_cells(puzzle, target_clues)
    return puzzle, solution
