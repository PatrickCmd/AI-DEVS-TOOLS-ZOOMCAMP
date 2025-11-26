import './App.css'
import { DirectionPad, GameBoard } from './components'
import { useSnakeGame } from './hooks'

const statusLabel = {
  idle: 'Idle',
  playing: 'Playing',
  paused: 'Paused',
  gameover: 'Game Over',
}

function App() {
  const {
    state,
    config,
    start,
    pause,
    resume,
    restart,
    requestDirection,
    soundEnabled,
    toggleSound,
    mode,
    changeMode,
  } = useSnakeGame()

  const startLabel = state.status === 'paused' ? 'Resume' : state.status === 'gameover' ? 'Restart' : 'Start'

  return (
    <div className="app">
      <header className="app__header">
        <p className="eyebrow">Snake · React + Vite</p>
        <h1>Snake</h1>
        <p className="lede">Classic arcade snake, built incrementally.</p>
      </header>

      <main className="app__grid">
        <section className="panel panel--board">
          <div className="panel__title">Game board</div>
          <GameBoard config={config} snake={state.snake} food={state.food} status={state.status} />
        </section>

        <aside className="panel panel--sidebar">
          <div>
            <div className="panel__title">HUD</div>
            <div className="hud">
              <div className="hud__row">
                <span>Score</span>
                <span>{state.score}</span>
              </div>
              <div className="hud__row">
                <span>High Score</span>
                <span>{state.highScore}</span>
              </div>
              <div className="hud__row">
                <span>Status</span>
                <span>{statusLabel[state.status]}</span>
              </div>
              <div className="hud__row">
                <span>Speed (ms)</span>
                <span>{state.status === 'idle' ? '—' : Math.round(state.speed)}</span>
              </div>
            </div>
          </div>

          <div>
            <div className="panel__title">Controls</div>
            <div className="controls">
              <button
                type="button"
                onClick={state.status === 'paused' ? resume : start}
                disabled={state.status === 'playing'}
              >
                {startLabel}
              </button>
              <button type="button" onClick={pause} disabled={state.status !== 'playing'}>
                Pause
              </button>
              <button type="button" onClick={restart}>
                Restart
              </button>
            </div>
            <div className="mode-toggle">
              <span className="mode-toggle__label">Mode</span>
              <label>
                <input
                  type="radio"
                  name="mode"
                  value="walls"
                  checked={mode === 'walls'}
                  onChange={() => changeMode('walls')}
                />
                Walls (classic)
              </label>
              <label>
                <input
                  type="radio"
                  name="mode"
                  value="pass"
                  checked={mode === 'pass-through'}
                  onChange={() => changeMode('pass-through')}
                />
                Pass-through (wrap edges)
              </label>
            </div>
            <div className="sound-toggle">
              <label>
                <input type="checkbox" checked={soundEnabled} onChange={toggleSound} />
                Sound effects
              </label>
            </div>
            <p className="helper-text">
              Use Arrow keys or WASD to steer. Avoid walls and your tail. Eating food grows the snake and speeds it up.
            </p>
            <div className="direction-pad__label">Touch / on-screen controls</div>
            <DirectionPad onDirection={requestDirection} disabled={state.status !== 'playing'} />
          </div>
        </aside>
      </main>
    </div>
  )
}

export default App
