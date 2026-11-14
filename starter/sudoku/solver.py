"""Sudoku board solving primitives."""

import random

from sudoku import EMPTY, SIZE


def is_safe(board: list[list[int]], row: int, col: int, num: int) -> bool:
    """Return whether a number can be placed at the given board position."""
    for index in range(SIZE):
        if board[row][index] == num or board[index][col] == num:
            return False

    box_row = row - row % 3
    box_col = col - col % 3
    for row_offset in range(3):
        for col_offset in range(3):
            if board[box_row + row_offset][box_col + col_offset] == num:
                return False
    return True


def fill_board(board: list[list[int]]) -> bool:
    """Fill an empty board with a valid Sudoku solution using backtracking."""
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                candidates = list(range(1, SIZE + 1))
                random.shuffle(candidates)
                for candidate in candidates:
                    if is_safe(board, row, col, candidate):
                        board[row][col] = candidate
                        if fill_board(board):
                            return True
                        board[row][col] = EMPTY
                return False
    return True
