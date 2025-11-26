import { DIRECTIONS } from '../utils/gameConfig';
import './Controls.css';

export const Controls = ({ changeDirection, status }) => {
  const handleDirectionClick = (direction) => {
    if (status === 'playing') {
      changeDirection(direction);
    }
  };

  return (
    <div className="controls">
      <div className="controls-row">
        <button
          className="control-btn"
          onClick={() => handleDirectionClick(DIRECTIONS.UP)}
          disabled={status !== 'playing'}
        >
          ▲
        </button>
      </div>
      <div className="controls-row">
        <button
          className="control-btn"
          onClick={() => handleDirectionClick(DIRECTIONS.LEFT)}
          disabled={status !== 'playing'}
        >
          ◄
        </button>
        <button
          className="control-btn"
          onClick={() => handleDirectionClick(DIRECTIONS.DOWN)}
          disabled={status !== 'playing'}
        >
          ▼
        </button>
        <button
          className="control-btn"
          onClick={() => handleDirectionClick(DIRECTIONS.RIGHT)}
          disabled={status !== 'playing'}
        >
          ►
        </button>
      </div>
    </div>
  );
};
