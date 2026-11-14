"""Interactive Sudoku game operations."""

import random

from sudoku import EMPTY, SIZE


def choose_hint(
    board: list[list[int]], solution: list[list[int]]
) -> tuple[int, int, int]:
    """Choose an empty cell and return its row, column, and solution value."""
    empty_cells = [
        (row, col)
        for row in range(SIZE)
        for col in range(SIZE)
        if board[row][col] == EMPTY
    ]
    if not empty_cells:
        raise ValueError("No empty cells available for a hint")

    row, col = random.choice(empty_cells)
    return row, col, solution[row][col]
