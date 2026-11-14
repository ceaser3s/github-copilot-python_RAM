"""Sudoku request-board validation helpers."""

from sudoku import SIZE


def validate_board(
    board: object,
) -> tuple[list[list[int]] | None, str | None]:
    """Check that a submitted board is a 9-by-9 grid of integers from 0 to 9."""
    if not isinstance(board, list) or len(board) != SIZE:
        return None, "Board must be a 9x9 grid of integers from 0 to 9"

    validated_board: list[list[int]] = []
    for row in board:
        if not isinstance(row, list) or len(row) != SIZE:
            return None, "Board must be a 9x9 grid of integers from 0 to 9"

        validated_row: list[int] = []
        for value in row:
            if (
                not isinstance(value, int)
                or isinstance(value, bool)
                or not 0 <= value <= SIZE
            ):
                return None, "Board must be a 9x9 grid of integers from 0 to 9"
            validated_row.append(value)
        validated_board.append(validated_row)
    return validated_board, None


def find_incorrect_cells(
    board: list[list[int]], solution: list[list[int]]
) -> list[list[int]]:
    """Return row and column coordinates where a board differs from a solution."""
    return [
        [row, col]
        for row in range(SIZE)
        for col in range(SIZE)
        if board[row][col] != solution[row][col]
    ]
