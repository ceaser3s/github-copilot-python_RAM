const STORAGE_KEY = 'sudokuTopTimes';
const MAX_ENTRIES = 10;

/**
 * Validate and normalize a list read from browser storage.
 * @param {unknown} entries Stored leaderboard value.
 * @returns {Array<{name: string, time: number, difficulty: string, hints: number}>}
 */
function normalizeEntries(entries) {
  if (!Array.isArray(entries)) return [];

  return entries
    .filter((entry) =>
      entry &&
      typeof entry.name === 'string' &&
      Number.isInteger(entry.time) &&
      entry.time >= 0 &&
      typeof entry.difficulty === 'string' &&
      Number.isInteger(entry.hints) &&
      entry.hints >= 0
    )
    .map((entry) => ({
      name: entry.name.trim() || 'Anonymous',
      time: entry.time,
      difficulty: entry.difficulty,
      hints: entry.hints
    }))
    .sort((first, second) => first.time - second.time)
    .slice(0, MAX_ENTRIES);
}

/**
 * Load and normalize leaderboard entries from localStorage.
 * @returns {Array<{name: string, time: number, difficulty: string, hints: number}>}
 */
export function loadLeaderboard() {
  try {
    const storedEntries = localStorage.getItem(STORAGE_KEY);
    return storedEntries ? normalizeEntries(JSON.parse(storedEntries)) : [];
  } catch (error) {
    console.error('Unable to load the Sudoku leaderboard.', error);
    return [];
  }
}

/**
 * Save leaderboard entries to localStorage.
 * @param {Array<{name: string, time: number, difficulty: string, hints: number}>} entries Entries to save.
 * @returns {boolean} Whether the entries were saved successfully.
 */
export function saveLeaderboard(entries) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(normalizeEntries(entries)));
    return true;
  } catch (error) {
    console.error('Unable to save the Sudoku leaderboard.', error);
    return false;
  }
}

/**
 * Check whether a completion time belongs in the Top 10.
 * @param {Array<{time: number}>} entries Current leaderboard.
 * @param {number} time Completion time in seconds.
 * @returns {boolean} Whether the time qualifies.
 */
export function qualifies(entries, time) {
  return entries.length < MAX_ENTRIES ||
    time < entries[entries.length - 1].time;
}

/**
 * Return the sorted Top 10 including a new score.
 * @param {Array<{name: string, time: number, difficulty: string, hints: number}>} entries Current leaderboard.
 * @param {{name: string, time: number, difficulty: string, hints: number}} entry New score.
 * @returns {Array<{name: string, time: number, difficulty: string, hints: number}>} Updated leaderboard.
 */
export function addEntry(entries, entry) {
  const name = typeof entry.name === 'string' ? entry.name.trim() : '';
  return normalizeEntries([...entries, {
    ...entry,
    name: name || 'Anonymous'
  }]);
}

/**
 * Format elapsed seconds as minutes and zero-padded seconds.
 * @param {number} seconds Elapsed time in seconds.
 * @returns {string} Time in m:ss format.
 */
export function formatTime(seconds) {
  const safeSeconds = Math.max(0, Math.floor(seconds));
  const minutes = Math.floor(safeSeconds / 60);
  const remainingSeconds = (safeSeconds % 60).toString().padStart(2, '0');
  return `${minutes}:${remainingSeconds}`;
}
