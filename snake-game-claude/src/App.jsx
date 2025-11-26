import { useSnakeGame } from './hooks/useSnakeGame';
import { useKeyboardControls } from './hooks/useKeyboardControls';
import { HUD } from './components/HUD';
import { GameBoard } from './components/GameBoard';
import { Controls } from './components/Controls';
import './App.css';

function App() {
  const {
    snake,
    food,
    status,
    score,
    gameMode,
    highScore,
    soundEnabled,
    changeDirection,
    setGameMode,
    toggleSound,
    startGame,
    pauseGame,
    resumeGame,
    restartGame,
  } = useSnakeGame();

  useKeyboardControls(changeDirection, status);

  return (
    <div className="app">
      <HUD
        score={score}
        highScore={highScore}
        status={status}
        gameMode={gameMode}
        soundEnabled={soundEnabled}
        onStart={startGame}
        onPause={pauseGame}
        onResume={resumeGame}
        onRestart={restartGame}
        onModeChange={setGameMode}
        onToggleSound={toggleSound}
      />

      <div className="game-container">
        <GameBoard snake={snake} food={food} />
      </div>

      <Controls changeDirection={changeDirection} status={status} />
    </div>
  );
}

export default App;
