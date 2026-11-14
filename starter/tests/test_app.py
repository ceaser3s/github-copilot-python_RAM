"""Baseline tests for the Flask routes."""

import pytest
from flask.testing import FlaskClient

import app as app_module


def test_home_returns_game_page(client: FlaskClient) -> None:
    """The home route renders the Sudoku game page."""
    response = client.get("/")

    assert response.status_code == 200
    assert b"Sudoku Game" in response.data


def test_new_game_returns_generated_puzzle(
    client: FlaskClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The new-game route returns the generated puzzle as JSON."""
    puzzle = [[0 for _ in range(9)] for _ in range(9)]
    solution = [
        [(row * 3 + row // 3 + col) % 9 + 1 for col in range(9)]
        for row in range(9)
    ]
    generated_clues = []

    def generate_puzzle(clues: int) -> tuple[list[list[int]], list[list[int]]]:
        generated_clues.append(clues)
        return puzzle, solution

    monkeypatch.setattr(
        app_module.sudoku_logic, "generate_puzzle", generate_puzzle
    )

    response = client.get("/new?clues=40")

    assert response.status_code == 200
    assert response.get_json() == {"puzzle": puzzle}
    assert generated_clues == [40]


def test_check_without_game_returns_error(client: FlaskClient) -> None:
    """The check route reports an error when no game has started."""
    response = client.post("/check", json={"board": [[0] * 9 for _ in range(9)]})

    assert response.status_code == 400
    assert response.get_json() == {"error": "No game in progress"}


def test_check_reports_incorrect_cells(
    client: FlaskClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The check route returns coordinates that differ from the solution."""
    puzzle = [[0 for _ in range(9)] for _ in range(9)]
    solution = [
        [(row * 3 + row // 3 + col) % 9 + 1 for col in range(9)]
        for row in range(9)
    ]
    monkeypatch.setattr(
        app_module.sudoku_logic,
        "generate_puzzle",
        lambda clues: (puzzle, solution),
    )
    client.get("/new")

    board = [row[:] for row in solution]
    board[2][4] = 0
    response = client.post("/check", json={"board": board})

    assert response.status_code == 200
    assert response.get_json() == {"incorrect": [[2, 4]]}
