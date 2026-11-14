"""Compatibility exports for callers of the legacy Sudoku logic module."""

from sudoku import EMPTY, SIZE
from sudoku.generator import (
    create_empty_board,
    deep_copy,
    generate_puzzle,
    remove_cells,
)
from sudoku.solver import fill_board, is_safe

__all__ = [
    "EMPTY",
    "SIZE",
    "create_empty_board",
    "deep_copy",
    "fill_board",
    "generate_puzzle",
    "is_safe",
    "remove_cells",
]
