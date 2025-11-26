import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { GameBoard } from './GameBoard';
import { BOARD_CONFIG } from '../utils/gameConfig';

describe('GameBoard', () => {
  const mockSnake = [
    { x: 10, y: 10 },
    { x: 9, y: 10 },
    { x: 8, y: 10 },
  ];

  const mockFood = { x: 15, y: 15 };

  it('should render without crashing', () => {
    const { container } = render(<GameBoard snake={mockSnake} food={mockFood} />);
    expect(container.querySelector('.game-board')).toBeInTheDocument();
  });

  it('should render correct number of rows', () => {
    const { container } = render(<GameBoard snake={mockSnake} food={mockFood} />);
    const rows = container.querySelectorAll('.board-row');
    expect(rows).toHaveLength(BOARD_CONFIG.rows);
  });

  it('should render correct number of cells per row', () => {
    const { container } = render(<GameBoard snake={mockSnake} food={mockFood} />);
    const firstRow = container.querySelector('.board-row');
    const cells = firstRow.querySelectorAll('.cell');
    expect(cells).toHaveLength(BOARD_CONFIG.cols);
  });

  it('should render total correct number of cells', () => {
    const { container } = render(<GameBoard snake={mockSnake} food={mockFood} />);
    const cells = container.querySelectorAll('.cell');
    expect(cells).toHaveLength(BOARD_CONFIG.rows * BOARD_CONFIG.cols);
  });

  it('should render snake head with correct class', () => {
    const { container } = render(<GameBoard snake={mockSnake} food={mockFood} />);
    const snakeHeadCells = container.querySelectorAll('.snake-head');
    expect(snakeHeadCells).toHaveLength(1);
  });

  it('should render snake body segments with correct class', () => {
    const { container } = render(<GameBoard snake={mockSnake} food={mockFood} />);
    const snakeBodyCells = container.querySelectorAll('.snake-body');
    // Snake has 3 segments: 1 head + 2 body
    expect(snakeBodyCells).toHaveLength(mockSnake.length - 1);
  });

  it('should render food with correct class', () => {
    const { container } = render(<GameBoard snake={mockSnake} food={mockFood} />);
    const foodCells = container.querySelectorAll('.food');
    expect(foodCells).toHaveLength(1);
  });

  it('should handle empty snake array', () => {
    const { container } = render(<GameBoard snake={[]} food={mockFood} />);
    const snakeHeadCells = container.querySelectorAll('.snake-head');
    const snakeBodyCells = container.querySelectorAll('.snake-body');
    expect(snakeHeadCells).toHaveLength(0);
    expect(snakeBodyCells).toHaveLength(0);
  });

  it('should handle null food', () => {
    const { container } = render(<GameBoard snake={mockSnake} food={null} />);
    const foodCells = container.querySelectorAll('.food');
    expect(foodCells).toHaveLength(0);
  });

  it('should render single-segment snake correctly', () => {
    const singleSegmentSnake = [{ x: 10, y: 10 }];
    const { container } = render(<GameBoard snake={singleSegmentSnake} food={mockFood} />);

    const snakeHeadCells = container.querySelectorAll('.snake-head');
    const snakeBodyCells = container.querySelectorAll('.snake-body');

    expect(snakeHeadCells).toHaveLength(1);
    expect(snakeBodyCells).toHaveLength(0);
  });
});
