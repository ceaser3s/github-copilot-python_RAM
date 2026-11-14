# Refactor a Sudoku Game written in Python Flask

Use this simple Sudoku game as a starting point to practice your skills with GitHub Copilot. The goal is to refactor the code to use modern technologies, while also adding new features and improving the overall user experience.

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Dependencies

```
- Modern web browser (Chrome, Firefox, Edge, etc.)
- Python 3
```

### Installation

1. Fork this repository to your GitHub account. (You can use the "Fork" button on the top right corner of the repository page.)

2. Clone your forked repository to your local machine.

3. Open a terminal window and navigate to the "github-copilot-python/starter" directory.

4. Create a Python virtual environment and activate it (optional but highly recommended).

```bash
python3 -m venv .venv
source .venv/bin/activate
```

5. Install required Python packages.

```bash
pip install -r requirements.txt
```

6. Run the Flask app.

```bash
python app.py
```

7. Open http://127.0.0.1:5000 in your browser.

## Project Instructions

Use GitHub Copilot to refactor the code for this game to add more advanced features. The goal is to create a more modern and maintainable codebase and add additional functionality to the final product. You can use any combination of code completion and chat features, like Ask, Edit, or Agent modes.

- Errors should be handled gracefully with appropriate messages to the user.
- Implement a Sudoku board generator that creates a valid Sudoku puzzle with a unique solution.
- Add a timer to track how long it takes to solve the puzzle.
- Implement a solution checker that verifies if the user's solution is correct using event delegation.
- Add a difficulty selector to allow users to choose between easy, medium, and hard puzzles.
- Add a hint feature that provides clues for the user that are noted with unique colors.
- Add a check puzzle button that checks the current state of the board against the solution.
- User should get immediate feedback on their input, such as highlighting invalid entries.
- Top 10 scores should be saved in local storage and displayed on the page with the user's name, time taken, hints used, and difficulty level.
- The game should be responsive and work well on both desktop and mobile devices.
- UI colors should be visually appealing and accessible.
- Completed and correct puzzles should display a congratulatory message with the time taken and hints used and ask for the user's name for Top 10 times.



## Running the tests
```bash
cd starter
pip install -r requirements.txt
python -m pytest
```



## Features
- Easy / Medium / Hard difficulty, and every puzzle has exactly one solution
- Locked prefilled cells, live conflict highlighting, Check and Hint buttons
- Timer, congratulatory message, and a Top 10 fastest times list saved in localStorage
- Light/dark mode toggle and a responsive layout with alternating 3x3 squares

## Project Structure
- `starter/app.py` – app factory and entry point
- `starter/routes.py` – Flask routes (Blueprint)
- `starter/sudoku/` – puzzle generator, solver (unique-solution check) and validator
- `starter/static/` – CSS and JavaScript (game logic, leaderboard, theme toggle)
- `starter/templates/` – HTML template
- `starter/tests/` – pytest tests
- `.github/copilot-instructions.md` – instructions for Copilot (copy in `instruction.md`)

## How I Used GitHub Copilot
Screenshots of my prompts and Copilot's responses are in the `Screenshots/` folder:
- Setting up the testing framework (`initial_tests.png`, `copilot_testing_framework_setup_*.png`)
- Refactoring into modules (`copilot_refactor_structure_*.png`)
- Unique-solution puzzles and difficulty levels (`copilot_unique_solution_*.png`)
- Hint, Check, live feedback and timer (`copilot_hint_check_feedback_*.png`)
- Top 10 scores in localStorage (`copilot_top10_localstorage_*.png`)
- Styling the 3x3 squares, dark mode and responsive layout (`copilot_3x3_square_colors_*.png`)

I reviewed each suggestion before accepting it. I rejected Copilot's request to create
`tasks.json` because it isn't needed for this project
(see `Screenshots/copilot_rejected_suggestion.png`).