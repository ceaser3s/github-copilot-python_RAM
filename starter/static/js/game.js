// Client-side rendering and interaction for the Flask-backed Sudoku.
const SIZE = 9;
let puzzle = [];
let hintsUsed = 0;
let elapsedSeconds = 0;
let timerInterval = null;
let completionCheckId = 0;
let gameCompleted = false;

function setMessage(text, kind = 'error') {
  const message = document.getElementById('message');
  message.innerText = text;
  message.className = text ? kind : '';
}

async function readJson(response) {
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || 'The request could not be completed.');
  }
  return data;
}

function formatTime(seconds) {
  const minutes = Math.floor(seconds / 60).toString().padStart(2, '0');
  const remainingSeconds = (seconds % 60).toString().padStart(2, '0');
  return `${minutes}:${remainingSeconds}`;
}

function updateTimer() {
  document.getElementById('timer').innerText = `Time: ${formatTime(elapsedSeconds)}`;
}

function stopTimer() {
  if (timerInterval !== null) {
    clearInterval(timerInterval);
    timerInterval = null;
  }
}

function startTimer() {
  stopTimer();
  elapsedSeconds = 0;
  gameCompleted = false;
  updateTimer();
  timerInterval = setInterval(() => {
    elapsedSeconds += 1;
    updateTimer();
  }, 1000);
}

function finishGame() {
  if (gameCompleted) return;
  gameCompleted = true;
  stopTimer();
  const hintLabel = hintsUsed === 1 ? 'hint' : 'hints';
  setMessage(
    `Congratulations! You solved it in ${formatTime(elapsedSeconds)} with ${hintsUsed} ${hintLabel}.`,
    'success'
  );
}

function getInputs() {
  return Array.from(document.querySelectorAll('.sudoku-cell'));
}

function getBoard() {
  const board = [];
  const inputs = getInputs();
  for (let row = 0; row < SIZE; row++) {
    board[row] = [];
    for (let col = 0; col < SIZE; col++) {
      const value = inputs[row * SIZE + col].value;
      board[row][col] = value ? Number.parseInt(value, 10) : 0;
    }
  }
  return board;
}

function isBoardFull(board) {
  return board.every((row) => row.every((value) => value !== 0));
}

function updateConflicts() {
  const inputs = getInputs();
  inputs.forEach((input) => input.classList.remove('conflict'));

  for (let first = 0; first < inputs.length; first++) {
    const firstInput = inputs[first];
    if (!firstInput.value) continue;

    const firstRow = Number(firstInput.dataset.row);
    const firstCol = Number(firstInput.dataset.col);
    for (let second = first + 1; second < inputs.length; second++) {
      const secondInput = inputs[second];
      if (firstInput.value !== secondInput.value) continue;

      const secondRow = Number(secondInput.dataset.row);
      const secondCol = Number(secondInput.dataset.col);
      const sameBox =
        Math.floor(firstRow / 3) === Math.floor(secondRow / 3) &&
        Math.floor(firstCol / 3) === Math.floor(secondCol / 3);
      if (
        firstRow === secondRow ||
        firstCol === secondCol ||
        sameBox
      ) {
        firstInput.classList.add('conflict');
        secondInput.classList.add('conflict');
      }
    }
  }
}

function createBoardElement() {
  const boardDiv = document.getElementById('sudoku-board');
  boardDiv.innerHTML = '';
  for (let row = 0; row < SIZE; row++) {
    const rowDiv = document.createElement('div');
    rowDiv.className = 'sudoku-row';
    for (let col = 0; col < SIZE; col++) {
      const input = document.createElement('input');
      input.type = 'text';
      input.inputMode = 'numeric';
      input.maxLength = 1;
      input.className = 'sudoku-cell';
      input.dataset.row = row;
      input.dataset.col = col;
      input.setAttribute('aria-label', `Row ${row + 1}, column ${col + 1}`);
      input.addEventListener('input', (event) => {
        const cell = event.currentTarget;
        cell.value = cell.value.replace(/[^1-9]/g, '');
        cell.classList.remove('incorrect');
        completionCheckId += 1;
        updateConflicts();
        const board = getBoard();
        if (isBoardFull(board)) verifyCompletion(board);
      });
      rowDiv.appendChild(input);
    }
    boardDiv.appendChild(rowDiv);
  }
}

function renderPuzzle(newPuzzle) {
  puzzle = newPuzzle;
  createBoardElement();
  const inputs = getInputs();
  for (let row = 0; row < SIZE; row++) {
    for (let col = 0; col < SIZE; col++) {
      const input = inputs[row * SIZE + col];
      const value = puzzle[row][col];
      input.value = value || '';
      input.readOnly = value !== 0;
      if (input.readOnly) input.classList.add('prefilled');
    }
  }
  updateConflicts();
}

async function newGame() {
  completionCheckId += 1;
  const difficulty = document.getElementById('difficulty').value;
  try {
    const response = await fetch(
      `/new?difficulty=${encodeURIComponent(difficulty)}`
    );
    const data = await readJson(response);
    renderPuzzle(data.puzzle);
    hintsUsed = 0;
    document.getElementById('hint-count').innerText = 'Hints used: 0';
    setMessage('');
    startTimer();
  } catch (error) {
    setMessage(error.message);
  }
}

async function checkSolution() {
  const board = getBoard();
  try {
    const response = await fetch('/check', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({board})
    });
    const data = await readJson(response);
    const inputs = getInputs();
    inputs.forEach((input) => input.classList.remove('incorrect'));
    const incorrect = new Set(
      data.incorrect.map(([row, col]) => row * SIZE + col)
    );
    incorrect.forEach((index) => inputs[index].classList.add('incorrect'));

    if (isBoardFull(board) && incorrect.size === 0) {
      finishGame();
    } else if (incorrect.size > 0) {
      setMessage('Some filled cells are incorrect.');
    } else {
      setMessage('Fill the remaining empty cells to finish.');
    }
  } catch (error) {
    setMessage(error.message);
  }
}

async function verifyCompletion(board) {
  const checkId = ++completionCheckId;
  try {
    const response = await fetch('/check', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({board})
    });
    const data = await readJson(response);
    if (checkId !== completionCheckId) return;
    const currentBoard = getBoard();
    if (
      isBoardFull(currentBoard) &&
      JSON.stringify(currentBoard) === JSON.stringify(board) &&
      data.incorrect.length === 0
    ) {
      finishGame();
    }
  } catch (error) {
    if (checkId === completionCheckId) setMessage(error.message);
  }
}

async function requestHint() {
  const board = getBoard();
  try {
    const response = await fetch('/hint', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({board})
    });
    const data = await readJson(response);
    const input = getInputs()[data.row * SIZE + data.col];
    input.value = data.value;
    input.readOnly = true;
    input.classList.add('hinted');
    hintsUsed = data.hints_used;
    document.getElementById('hint-count').innerText = `Hints used: ${hintsUsed}`;
    setMessage('');
    updateConflicts();
    const updatedBoard = getBoard();
    if (isBoardFull(updatedBoard)) verifyCompletion(updatedBoard);
  } catch (error) {
    setMessage(error.message);
  }
}

window.addEventListener('load', () => {
  document.getElementById('new-game').addEventListener('click', newGame);
  document.getElementById('check-solution').addEventListener('click', checkSolution);
  document.getElementById('hint').addEventListener('click', requestHint);
  newGame();
});
