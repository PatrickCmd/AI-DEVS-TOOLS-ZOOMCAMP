import { GAME_MODES } from '../utils/gameConfig';
import './HUD.css';

export const HUD = ({ score, highScore, status, gameMode, soundEnabled, onStart, onPause, onResume, onRestart, onModeChange, onToggleSound }) => {
  const getStatusText = () => {
    switch (status) {
      case 'idle':
        return 'Press Start to Play';
      case 'playing':
        return 'Playing...';
      case 'paused':
        return 'Paused';
      case 'gameover':
        return 'Game Over!';
      default:
        return '';
    }
  };

  return (
    <div className="hud">
      <div className="hud-header">
        <h1>Snake Game</h1>
        <button
          className="sound-toggle"
          onClick={onToggleSound}
          title={soundEnabled ? 'Sound On' : 'Sound Off'}
        >
          {soundEnabled ? '🔊' : '🔇'}
        </button>
      </div>

      <div className="hud-info">
        <div className="score-display">
          <div className="score-item">
            <span className="label">Score:</span>
            <span className="value">{score}</span>
          </div>
          <div className="score-item">
            <span className="label">High Score:</span>
            <span className="value high-score">{highScore}</span>
          </div>
        </div>
        <div className={`status-display status-${status}`}>
          {getStatusText()}
        </div>
        <div className="mode-selector">
          <span className="mode-label">Mode:</span>
          <div className="mode-buttons">
            <button
              className={`mode-btn ${gameMode === GAME_MODES.WALLS ? 'active' : ''}`}
              onClick={() => onModeChange(GAME_MODES.WALLS)}
              disabled={status === 'playing'}
            >
              Walls
            </button>
            <button
              className={`mode-btn ${gameMode === GAME_MODES.PASS_THROUGH ? 'active' : ''}`}
              onClick={() => onModeChange(GAME_MODES.PASS_THROUGH)}
              disabled={status === 'playing'}
            >
              Pass-Through
            </button>
          </div>
        </div>
      </div>

      <div className="hud-controls">
        {status === 'idle' && (
          <button className="btn btn-primary" onClick={onStart}>
            Start Game
          </button>
        )}

        {status === 'playing' && (
          <button className="btn btn-secondary" onClick={onPause}>
            Pause
          </button>
        )}

        {status === 'paused' && (
          <>
            <button className="btn btn-primary" onClick={onResume}>
              Resume
            </button>
            <button className="btn btn-secondary" onClick={onRestart}>
              Restart
            </button>
          </>
        )}

        {status === 'gameover' && (
          <button className="btn btn-primary" onClick={onRestart}>
            Play Again
          </button>
        )}
      </div>

      <div className="hud-instructions">
        <p>Use Arrow Keys or WASD to move</p>
      </div>
    </div>
  );
};
