"""HTTP routes for the Sudoku game."""

from typing import TypedDict

from flask import Blueprint, Response, jsonify, render_template, request

from sudoku import game, generator, validator

blueprint = Blueprint("sudoku", __name__)

# Keep the current game in memory to preserve the app's existing behavior.
class GameState(TypedDict):
    """State retained for the active Sudoku game."""

    puzzle: list[list[int]] | None
    solution: list[list[int]] | None
    hints_used: int
    hint_cells: list[list[int]]


CURRENT: GameState = {
    "puzzle": None,
    "solution": None,
    "hints_used": 0,
    "hint_cells": [],
}


@blueprint.route("/")
def index() -> str:
    """Render the Sudoku game page."""
    return render_template("index.html")


@blueprint.route("/new")
def new_game() -> Response | tuple[Response, int]:
    """Generate a puzzle at the requested difficulty and return it as JSON."""
    difficulty = request.args.get("difficulty", "medium").lower()
    if difficulty not in generator.DIFFICULTY_CLUES:
        return (
            jsonify({"error": "Difficulty must be one of: easy, medium, hard"}),
            400,
        )

    if "clues" in request.args:
        clues_value = request.args["clues"]
        try:
            clues = int(clues_value)
        except ValueError:
            return (
                jsonify({"error": "Clues must be an integer between 0 and 81"}),
                400,
            )

        if not 0 <= clues <= generator.SIZE * generator.SIZE:
            return (
                jsonify({"error": "Clues must be an integer between 0 and 81"}),
                400,
            )
        puzzle, solution = generator.generate_puzzle(clues)
    else:
        puzzle, solution = generator.generate_puzzle(difficulty)

    CURRENT["puzzle"] = puzzle
    CURRENT["solution"] = solution
    CURRENT["hints_used"] = 0
    CURRENT["hint_cells"] = []
    return jsonify({"puzzle": puzzle})


@blueprint.route("/check", methods=["POST"])
def check_solution() -> Response | tuple[Response, int]:
    """Return coordinates of board cells that differ from the solution."""
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object"}), 400

    solution = CURRENT.get("solution")
    if solution is None:
        return jsonify({"error": "No game in progress"}), 400

    board, error = validator.validate_board(data.get("board"))
    if board is None:
        return jsonify({"error": error}), 400

    return jsonify({"incorrect": validator.find_incorrect_cells(board, solution)})


@blueprint.route("/hint", methods=["POST"])
def get_hint() -> Response | tuple[Response, int]:
    """Fill one empty cell using the active game's stored solution."""
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object"}), 400

    solution = CURRENT["solution"]
    if solution is None:
        return jsonify({"error": "No game in progress"}), 400

    board, error = validator.validate_board(data.get("board"))
    if board is None:
        return jsonify({"error": error}), 400

    try:
        row, col, value = game.choose_hint(board, solution)
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    CURRENT["hints_used"] += 1
    CURRENT["hint_cells"].append([row, col])
    return jsonify(
        {
            "row": row,
            "col": col,
            "value": value,
            "hints_used": CURRENT["hints_used"],
        }
    )
