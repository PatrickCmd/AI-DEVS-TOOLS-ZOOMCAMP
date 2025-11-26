const STORAGE_KEYS = {
  HIGH_SCORE: 'snake-game-high-score',
  SOUND_ENABLED: 'snake-game-sound-enabled',
};

/**
 * Get high score from localStorage
 */
export const getHighScore = () => {
  try {
    const stored = localStorage.getItem(STORAGE_KEYS.HIGH_SCORE);
    return stored ? parseInt(stored, 10) : 0;
  } catch (error) {
    console.error('Error reading high score from localStorage:', error);
    return 0;
  }
};

/**
 * Save high score to localStorage
 */
export const saveHighScore = (score) => {
  try {
    localStorage.setItem(STORAGE_KEYS.HIGH_SCORE, score.toString());
  } catch (error) {
    console.error('Error saving high score to localStorage:', error);
  }
};

/**
 * Update high score if current score is higher
 */
export const updateHighScore = (currentScore) => {
  const highScore = getHighScore();
  if (currentScore > highScore) {
    saveHighScore(currentScore);
    return true; // New high score!
  }
  return false;
};

/**
 * Get sound enabled preference from localStorage
 */
export const getSoundEnabled = () => {
  try {
    const stored = localStorage.getItem(STORAGE_KEYS.SOUND_ENABLED);
    return stored !== null ? stored === 'true' : true; // Default to enabled
  } catch (error) {
    console.error('Error reading sound preference from localStorage:', error);
    return true;
  }
};

/**
 * Save sound enabled preference to localStorage
 */
export const setSoundEnabled = (enabled) => {
  try {
    localStorage.setItem(STORAGE_KEYS.SOUND_ENABLED, enabled.toString());
  } catch (error) {
    console.error('Error saving sound preference to localStorage:', error);
  }
};
