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


def count_solutions(board: list[list[int]], limit: int = 2) -> int:
    """Count board solutions, stopping once ``limit`` solutions are found."""
    if (
        limit <= 0
        or len(board) != SIZE
        or any(len(row) != SIZE for row in board)
    ):
        return 0

    for row in range(SIZE):
        row_values: set[int] = set()
        column_values: set[int] = set()
        for index in range(SIZE):
            row_value = board[row][index]
            column_value = board[index][row]
            if not 0 <= row_value <= SIZE or not 0 <= column_value <= SIZE:
                return 0
            if row_value and row_value in row_values:
                return 0
            if column_value and column_value in column_values:
                return 0
            if row_value:
                row_values.add(row_value)
            if column_value:
                column_values.add(column_value)

    for box_row in range(0, SIZE, 3):
        for box_col in range(0, SIZE, 3):
            box_values: set[int] = set()
            for row_offset in range(3):
                for col_offset in range(3):
                    value = board[box_row + row_offset][box_col + col_offset]
                    if value and value in box_values:
                        return 0
                    if value:
                        box_values.add(value)

    solutions = 0

    def search() -> None:
        """Find solutions using the most constrained empty cell first."""
        nonlocal solutions
        if solutions >= limit:
            return

        best_position: tuple[int, int] | None = None
        best_candidates: list[int] | None = None
        for row in range(SIZE):
            for col in range(SIZE):
                if board[row][col] != EMPTY:
                    continue
                candidates = [
                    number
                    for number in range(1, SIZE + 1)
                    if is_safe(board, row, col, number)
                ]
                if not candidates:
                    return
                if (
                    best_candidates is None
                    or len(candidates) < len(best_candidates)
                ):
                    best_position = (row, col)
                    best_candidates = candidates
                    if len(candidates) == 1:
                        break
            if best_candidates is not None and len(best_candidates) == 1:
                break

        if best_position is None:
            solutions += 1
            return

        row, col = best_position
        for candidate in best_candidates or []:
            board[row][col] = candidate
            search()
            board[row][col] = EMPTY
            if solutions >= limit:
                return

    search()
    return solutions
