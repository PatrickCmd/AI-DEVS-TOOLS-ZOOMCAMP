import { BOARD_CONFIG } from '../utils/gameConfig';
import { getCellId, isSamePosition } from '../utils/coordinateHelpers';
import './GameBoard.css';

export const GameBoard = ({ snake, food }) => {
  const renderCell = (x, y) => {
    const position = { x, y };
    const isSnakeHead = snake.length > 0 && isSamePosition(snake[0], position);
    const isSnakeBody = snake.slice(1).some(segment => isSamePosition(segment, position));
    const isFood = food && isSamePosition(food, position);

    let cellClass = 'cell';
    if (isSnakeHead) cellClass += ' snake-head';
    else if (isSnakeBody) cellClass += ' snake-body';
    else if (isFood) cellClass += ' food';

    return (
      <div
        key={getCellId(x, y)}
        className={cellClass}
      />
    );
  };

  const renderRow = (y) => {
    const cells = [];
    for (let x = 0; x < BOARD_CONFIG.cols; x++) {
      cells.push(renderCell(x, y));
    }
    return (
      <div key={`row-${y}`} className="board-row">
        {cells}
      </div>
    );
  };

  const renderBoard = () => {
    const rows = [];
    for (let y = 0; y < BOARD_CONFIG.rows; y++) {
      rows.push(renderRow(y));
    }
    return rows;
  };

  return (
    <div className="game-board">
      {renderBoard()}
    </div>
  );
};
