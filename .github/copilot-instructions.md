# Copilot Instructions: Flask Sudoku Refactor

## Project goal
Refactor a legacy Python Sudoku game into a modern, modular Flask app with:
difficulty levels (Easy/Medium/Hard), puzzles with exactly one unique solution,
instant invalid-move feedback, Hint and Check buttons, a timer, a Top 10
fastest-times list saved in localStorage (name, time, difficulty, hints),
a completion message, and a light/dark mode toggle.

## Tech stack
- Backend: Python 3, Flask
- Frontend: plain HTML, CSS and vanilla JavaScript (no frameworks)
- Tests: pytest

## Code style
- Readable, consistent and maintainable code over clever code.
- Python: PEP 8, type hints, f-strings, docstrings on every function and class.
- JavaScript: ES6+ (const/let, arrow functions, modules), no global variables.
- Small single-purpose functions. No duplicated logic.
- Add short comments that explain why, not what.
- Use consistent error handling: validate input, return clear JSON errors from
  Flask routes, and use try/catch around localStorage access in JavaScript.

## Structure
- Separate puzzle generation, solving/validation and Flask routes into
  different modules.
- Keep templates in templates/, CSS and JS in static/, tests in tests/.
- Do not put game logic inside route functions.

## Game rules
- Each puzzle must have exactly one solution. Verify with a solution counter.
- Prefilled cells are locked (read-only).

- Hint fills one correct empty cell and locks it. Count hints used.
- Check highlights incorrect entries.
- Highlight row/column/square conflicts immediately when a number is entered.

## UI rules
- Plain CSS with CSS variables for theming.
- Must look good in light and dark mode, and text and buttons must stay readable.
- Responsive: scales smoothly between mobile and desktop.
- Alternate background colors on the 3x3 squares. No layout shift.
- Use semantic HTML and keep controls keyboard accessible.

## Testing
- Run pytest after every change. Add tests for new features.
- Do not break existing tests. If a test fails, explain why before fixing.

## How to respond
- Make the smallest change that solves the problem. Do not rewrite unrelated code.
- Explain any suggestion that uses unfamiliar syntax or libraries.
- Prefer modern language features.
