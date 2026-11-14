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


def test_new_game_rejects_invalid_difficulty(client: FlaskClient) -> None:
    """The new-game route rejects unsupported difficulty values."""
    response = client.get("/new?difficulty=impossible")

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "Difficulty must be one of: easy, medium, hard"
    }


def test_new_game_uses_requested_difficulty(
    client: FlaskClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The new-game route forwards a selected difficulty to generation."""
    puzzle = [[0 for _ in range(9)] for _ in range(9)]
    solution = [[1 for _ in range(9)] for _ in range(9)]
    selected_difficulties = []

    def generate_puzzle(difficulty: str) -> tuple[list[list[int]], list[list[int]]]:
        selected_difficulties.append(difficulty)
        return puzzle, solution

    monkeypatch.setattr(
        app_module.sudoku_logic, "generate_puzzle", generate_puzzle
    )

    response = client.get("/new?difficulty=hard")

    assert response.status_code == 200
    assert selected_difficulties == ["hard"]


def test_new_game_defaults_to_medium(
    client: FlaskClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The new-game route selects medium when difficulty is omitted."""
    selected_difficulties = []

    def generate_puzzle(difficulty: str) -> tuple[list[list[int]], list[list[int]]]:
        selected_difficulties.append(difficulty)
        return [[0] * 9 for _ in range(9)], [[1] * 9 for _ in range(9)]

    monkeypatch.setattr(
        app_module.sudoku_logic, "generate_puzzle", generate_puzzle
    )

    response = client.get("/new")

    assert response.status_code == 200
    assert selected_difficulties == ["medium"]


def test_check_without_game_returns_error(client: FlaskClient) -> None:
    """The check route reports an error when no game has started."""
    response = client.post("/check", json={"board": [[0] * 9 for _ in range(9)]})

    assert response.status_code == 400
    assert response.get_json() == {"error": "No game in progress"}


def test_check_reports_incorrect_cells(
    client: FlaskClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Check reports wrong filled cells but ignores empty cells."""
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
    board[2][4] = solution[2][4] % 9 + 1
    board[1][1] = 0
    response = client.post("/check", json={"board": board})

    assert response.status_code == 200
    assert response.get_json() == {"incorrect": [[2, 4]]}


def test_hint_fills_correct_empty_cell_and_increments_count(
    client: FlaskClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A hint returns the solution value and increments the game's count."""
    puzzle = [[0 for _ in range(9)] for _ in range(9)]
    solution = [
        [(row * 3 + row // 3 + col) % 9 + 1 for col in range(9)]
        for row in range(9)
    ]
    monkeypatch.setattr(
        app_module.sudoku_logic,
        "generate_puzzle",
        lambda difficulty: (puzzle, solution),
    )
    client.get("/new")

    response = client.post("/hint", json={"board": puzzle})
    data = response.get_json()

    assert response.status_code == 200
    assert data is not None
    assert puzzle[data["row"]][data["col"]] == 0
    assert data["value"] == solution[data["row"]][data["col"]]
    assert data["hints_used"] == 1
    assert app_module.CURRENT["hints_used"] == 1
    assert [data["row"], data["col"]] in app_module.CURRENT["hint_cells"]


def test_hint_on_full_board_returns_error(client: FlaskClient) -> None:
    """The hint route rejects a board without any empty cells."""
    puzzle = [[0 for _ in range(9)] for _ in range(9)]
    solution = [
        [(row * 3 + row // 3 + col) % 9 + 1 for col in range(9)]
        for row in range(9)
    ]
    app_module.CURRENT.update(puzzle=puzzle, solution=solution)

    response = client.post("/hint", json={"board": solution})

    assert response.status_code == 400
    assert response.get_json() == {"error": "No empty cells available for a hint"}
    assert app_module.CURRENT["hints_used"] == 0
