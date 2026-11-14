"""Tests for Sudoku solution counting and puzzle generation."""

import random

import pytest

from sudoku.generator import DIFFICULTY_CLUES, generate_puzzle
from sudoku.solver import count_solutions


@pytest.mark.parametrize("difficulty", ["easy", "medium", "hard"])
def test_generated_puzzles_are_unique_and_match_difficulty(
    difficulty: str,
) -> None:
    """Generated puzzles remain unique and near their clue-count target."""
    random.seed(314)

    puzzle, _ = generate_puzzle(difficulty)
    clue_count = sum(value != 0 for row in puzzle for value in row)

    assert count_solutions(puzzle) == 1
    assert (
        DIFFICULTY_CLUES[difficulty]
        <= clue_count
        <= DIFFICULTY_CLUES[difficulty] + 8
    )


def test_count_solutions_stops_at_limit_without_changing_board() -> None:
    """Counting an underconstrained board respects its limit and restores it."""
    board = [[0 for _ in range(9)] for _ in range(9)]

    assert count_solutions(board, limit=2) == 2
    assert board == [[0 for _ in range(9)] for _ in range(9)]
