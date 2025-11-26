// Board configuration
export const BOARD_CONFIG = {
  rows: 20,
  cols: 20,
  cellSize: 20, // pixels
};

// Game directions
export const DIRECTIONS = {
  UP: { x: 0, y: -1 },
  DOWN: { x: 0, y: 1 },
  LEFT: { x: -1, y: 0 },
  RIGHT: { x: 1, y: 0 },
};

// Initial game speed (ms per tick)
export const INITIAL_SPEED = 150;

// Speed increase per food eaten
export const SPEED_INCREMENT = 5;

// Minimum speed (fastest)
export const MIN_SPEED = 50;

// Game modes
export const GAME_MODES = {
  WALLS: 'walls',
  PASS_THROUGH: 'pass-through',
};

// Default game mode
export const DEFAULT_MODE = GAME_MODES.WALLS;
