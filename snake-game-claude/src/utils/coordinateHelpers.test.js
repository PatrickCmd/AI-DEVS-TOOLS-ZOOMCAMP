import { describe, it, expect } from 'vitest';
import {
  getCellId,
  isWithinBounds,
  isSamePosition,
  getRandomEmptyCell,
  isCollisionWithSnake,
  getInitialSnakePosition,
  wrapCoordinates,
} from './coordinateHelpers';
import { BOARD_CONFIG } from './gameConfig';

describe('coordinateHelpers', () => {
  describe('getCellId', () => {
    it('should return a unique cell ID for given coordinates', () => {
      expect(getCellId(5, 10)).toBe('5-10');
      expect(getCellId(0, 0)).toBe('0-0');
      expect(getCellId(19, 19)).toBe('19-19');
    });
  });

  describe('isWithinBounds', () => {
    it('should return true for coordinates within bounds', () => {
      expect(isWithinBounds(0, 0)).toBe(true);
      expect(isWithinBounds(10, 10)).toBe(true);
      expect(isWithinBounds(19, 19)).toBe(true);
    });

    it('should return false for coordinates outside bounds', () => {
      expect(isWithinBounds(-1, 0)).toBe(false);
      expect(isWithinBounds(0, -1)).toBe(false);
      expect(isWithinBounds(20, 10)).toBe(false);
      expect(isWithinBounds(10, 20)).toBe(false);
      expect(isWithinBounds(25, 25)).toBe(false);
    });
  });

  describe('isSamePosition', () => {
    it('should return true for identical positions', () => {
      expect(isSamePosition({ x: 5, y: 5 }, { x: 5, y: 5 })).toBe(true);
      expect(isSamePosition({ x: 0, y: 0 }, { x: 0, y: 0 })).toBe(true);
    });

    it('should return false for different positions', () => {
      expect(isSamePosition({ x: 5, y: 5 }, { x: 5, y: 6 })).toBe(false);
      expect(isSamePosition({ x: 5, y: 5 }, { x: 6, y: 5 })).toBe(false);
      expect(isSamePosition({ x: 1, y: 1 }, { x: 2, y: 2 })).toBe(false);
    });
  });

  describe('getRandomEmptyCell', () => {
    it('should return a position within bounds', () => {
      const occupiedCells = new Set();
      const emptyCell = getRandomEmptyCell(occupiedCells);

      expect(emptyCell).toBeDefined();
      expect(isWithinBounds(emptyCell.x, emptyCell.y)).toBe(true);
    });

    it('should not return an occupied position', () => {
      const occupiedCells = new Set(['5-5', '6-6', '7-7']);
      const emptyCell = getRandomEmptyCell(occupiedCells);

      expect(emptyCell).toBeDefined();
      const cellId = getCellId(emptyCell.x, emptyCell.y);
      expect(occupiedCells.has(cellId)).toBe(false);
    });

    it('should return null when board is full', () => {
      const occupiedCells = new Set();
      // Fill entire board
      for (let y = 0; y < BOARD_CONFIG.rows; y++) {
        for (let x = 0; x < BOARD_CONFIG.cols; x++) {
          occupiedCells.add(getCellId(x, y));
        }
      }

      const emptyCell = getRandomEmptyCell(occupiedCells);
      expect(emptyCell).toBeNull();
    });
  });

  describe('isCollisionWithSnake', () => {
    const snake = [
      { x: 5, y: 5 },
      { x: 4, y: 5 },
      { x: 3, y: 5 },
    ];

    it('should return true when position collides with snake', () => {
      expect(isCollisionWithSnake({ x: 5, y: 5 }, snake)).toBe(true);
      expect(isCollisionWithSnake({ x: 4, y: 5 }, snake)).toBe(true);
      expect(isCollisionWithSnake({ x: 3, y: 5 }, snake)).toBe(true);
    });

    it('should return false when position does not collide with snake', () => {
      expect(isCollisionWithSnake({ x: 6, y: 5 }, snake)).toBe(false);
      expect(isCollisionWithSnake({ x: 5, y: 6 }, snake)).toBe(false);
      expect(isCollisionWithSnake({ x: 10, y: 10 }, snake)).toBe(false);
    });
  });

  describe('getInitialSnakePosition', () => {
    it('should return a snake with 3 segments', () => {
      const snake = getInitialSnakePosition();
      expect(snake).toHaveLength(3);
    });

    it('should return snake in center of board', () => {
      const snake = getInitialSnakePosition();
      const centerX = Math.floor(BOARD_CONFIG.cols / 2);
      const centerY = Math.floor(BOARD_CONFIG.rows / 2);

      expect(snake[0]).toEqual({ x: centerX, y: centerY });
      expect(snake[1]).toEqual({ x: centerX - 1, y: centerY });
      expect(snake[2]).toEqual({ x: centerX - 2, y: centerY });
    });

    it('should return snake segments within bounds', () => {
      const snake = getInitialSnakePosition();
      snake.forEach(segment => {
        expect(isWithinBounds(segment.x, segment.y)).toBe(true);
      });
    });
  });

  describe('wrapCoordinates', () => {
    it('should return same coordinates when within bounds', () => {
      expect(wrapCoordinates(10, 10)).toEqual({ x: 10, y: 10 });
      expect(wrapCoordinates(0, 0)).toEqual({ x: 0, y: 0 });
      expect(wrapCoordinates(19, 19)).toEqual({ x: 19, y: 19 });
    });

    it('should wrap negative x to right edge', () => {
      const result = wrapCoordinates(-1, 10);
      expect(result).toEqual({ x: BOARD_CONFIG.cols - 1, y: 10 });
    });

    it('should wrap x beyond right edge to left edge', () => {
      const result = wrapCoordinates(BOARD_CONFIG.cols, 10);
      expect(result).toEqual({ x: 0, y: 10 });
    });

    it('should wrap negative y to bottom edge', () => {
      const result = wrapCoordinates(10, -1);
      expect(result).toEqual({ x: 10, y: BOARD_CONFIG.rows - 1 });
    });

    it('should wrap y beyond bottom edge to top edge', () => {
      const result = wrapCoordinates(10, BOARD_CONFIG.rows);
      expect(result).toEqual({ x: 10, y: 0 });
    });

    it('should wrap both coordinates simultaneously', () => {
      const result = wrapCoordinates(-1, -1);
      expect(result).toEqual({
        x: BOARD_CONFIG.cols - 1,
        y: BOARD_CONFIG.rows - 1
      });
    });

    it('should wrap when going beyond both edges', () => {
      const result = wrapCoordinates(BOARD_CONFIG.cols, BOARD_CONFIG.rows);
      expect(result).toEqual({ x: 0, y: 0 });
    });
  });
});
