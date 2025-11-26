import { BOARD_CONFIG } from './gameConfig';

/**
 * Convert grid coordinates to a unique cell ID
 */
export const getCellId = (x, y) => `${x}-${y}`;

/**
 * Check if coordinates are within board bounds
 */
export const isWithinBounds = (x, y) => {
  return x >= 0 && x < BOARD_CONFIG.cols && y >= 0 && y < BOARD_CONFIG.rows;
};

/**
 * Check if two positions are equal
 */
export const isSamePosition = (pos1, pos2) => {
  return pos1.x === pos2.x && pos1.y === pos2.y;
};

/**
 * Get a random empty cell that's not occupied by the snake
 */
export const getRandomEmptyCell = (occupiedCells) => {
  const emptyCells = [];

  for (let y = 0; y < BOARD_CONFIG.rows; y++) {
    for (let x = 0; x < BOARD_CONFIG.cols; x++) {
      const cellId = getCellId(x, y);
      if (!occupiedCells.has(cellId)) {
        emptyCells.push({ x, y });
      }
    }
  }

  if (emptyCells.length === 0) {
    return null; // Board is full
  }

  const randomIndex = Math.floor(Math.random() * emptyCells.length);
  return emptyCells[randomIndex];
};

/**
 * Check if a position collides with the snake body
 */
export const isCollisionWithSnake = (position, snake) => {
  return snake.some(segment => isSamePosition(segment, position));
};

/**
 * Wrap coordinates to opposite side (for pass-through mode)
 */
export const wrapCoordinates = (x, y) => {
  let wrappedX = x;
  let wrappedY = y;

  if (x < 0) wrappedX = BOARD_CONFIG.cols - 1;
  if (x >= BOARD_CONFIG.cols) wrappedX = 0;
  if (y < 0) wrappedY = BOARD_CONFIG.rows - 1;
  if (y >= BOARD_CONFIG.rows) wrappedY = 0;

  return { x: wrappedX, y: wrappedY };
};

/**
 * Get initial snake position (center of board)
 */
export const getInitialSnakePosition = () => {
  const centerX = Math.floor(BOARD_CONFIG.cols / 2);
  const centerY = Math.floor(BOARD_CONFIG.rows / 2);

  return [
    { x: centerX, y: centerY },
    { x: centerX - 1, y: centerY },
    { x: centerX - 2, y: centerY },
  ];
};
