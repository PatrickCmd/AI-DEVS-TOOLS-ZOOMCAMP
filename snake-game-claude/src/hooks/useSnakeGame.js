import { useState, useEffect, useCallback, useRef } from 'react';
import { DIRECTIONS, INITIAL_SPEED, SPEED_INCREMENT, MIN_SPEED, GAME_MODES, DEFAULT_MODE } from '../utils/gameConfig';
import {
  getInitialSnakePosition,
  getRandomEmptyCell,
  getCellId,
  isWithinBounds,
  isSamePosition,
  isCollisionWithSnake,
  wrapCoordinates,
} from '../utils/coordinateHelpers';
import { getHighScore, updateHighScore, getSoundEnabled, setSoundEnabled } from '../utils/storage';
import { playSound } from '../utils/sounds';

export const useSnakeGame = () => {
  const [snake, setSnake] = useState(getInitialSnakePosition());
  const [direction, setDirection] = useState(DIRECTIONS.RIGHT);
  const [food, setFood] = useState(null);
  const [status, setStatus] = useState('idle'); // 'idle' | 'playing' | 'paused' | 'gameover'
  const [score, setScore] = useState(0);
  const [speed, setSpeed] = useState(INITIAL_SPEED);
  const [gameMode, setGameMode] = useState(DEFAULT_MODE);
  const [highScore, setHighScore] = useState(getHighScore());
  const [soundEnabled, setSoundEnabledState] = useState(getSoundEnabled());

  const directionRef = useRef(direction);
  const statusRef = useRef(status);
  const gameModeRef = useRef(gameMode);
  const soundEnabledRef = useRef(soundEnabled);

  // Keep refs in sync with state for use in interval
  useEffect(() => {
    directionRef.current = direction;
  }, [direction]);

  useEffect(() => {
    statusRef.current = status;
  }, [status]);

  useEffect(() => {
    gameModeRef.current = gameMode;
  }, [gameMode]);

  useEffect(() => {
    soundEnabledRef.current = soundEnabled;
  }, [soundEnabled]);

  // Initialize food on first render
  useEffect(() => {
    if (!food) {
      spawnFood(snake);
    }
  }, [food, snake]);

  // Spawn food at a random empty cell
  const spawnFood = useCallback((currentSnake) => {
    const occupiedCells = new Set(
      currentSnake.map(segment => getCellId(segment.x, segment.y))
    );
    const newFood = getRandomEmptyCell(occupiedCells);
    if (newFood) {
      setFood(newFood);
    }
  }, []);

  // Change direction (prevent 180-degree turns)
  const changeDirection = useCallback((newDirection) => {
    const current = directionRef.current;

    // Prevent reversing direction
    if (
      (current === DIRECTIONS.UP && newDirection === DIRECTIONS.DOWN) ||
      (current === DIRECTIONS.DOWN && newDirection === DIRECTIONS.UP) ||
      (current === DIRECTIONS.LEFT && newDirection === DIRECTIONS.RIGHT) ||
      (current === DIRECTIONS.RIGHT && newDirection === DIRECTIONS.LEFT)
    ) {
      return;
    }

    setDirection(newDirection);
  }, []);

  // Game loop tick
  const tick = useCallback(() => {
    if (statusRef.current !== 'playing') return;

    setSnake(prevSnake => {
      const head = prevSnake[0];
      const currentDirection = directionRef.current;
      const currentMode = gameModeRef.current;

      // Calculate new head position
      let newHead = {
        x: head.x + currentDirection.x,
        y: head.y + currentDirection.y,
      };

      // Handle boundary based on game mode
      if (!isWithinBounds(newHead.x, newHead.y)) {
        if (currentMode === GAME_MODES.WALLS) {
          // Wall collision - game over
          playSound('gameOver', soundEnabledRef.current);
          setStatus('gameover');
          return prevSnake;
        } else {
          // Pass-through mode - wrap around
          newHead = wrapCoordinates(newHead.x, newHead.y);
        }
      }

      // Check self collision
      if (isCollisionWithSnake(newHead, prevSnake)) {
        playSound('gameOver', soundEnabledRef.current);
        setStatus('gameover');
        return prevSnake;
      }

      // Create new snake with new head
      const newSnake = [newHead, ...prevSnake];

      // Check if food is eaten
      if (food && isSamePosition(newHead, food)) {
        // Grow snake (don't remove tail)
        const newScore = prevSnake.length; // Score is snake length - 1 (for original length)
        setScore(newScore);

        // Play eat sound
        playSound('eat', soundEnabledRef.current);

        // Check for high score
        const isNewHighScore = updateHighScore(newScore);
        if (isNewHighScore) {
          setHighScore(newScore);
          playSound('newHighScore', soundEnabledRef.current);
        }

        // Increase speed
        setSpeed(prev => Math.max(MIN_SPEED, prev - SPEED_INCREMENT));

        // Spawn new food
        spawnFood(newSnake);

        return newSnake;
      } else {
        // Remove tail (no growth)
        newSnake.pop();
        return newSnake;
      }
    });
  }, [food, spawnFood]);

  // Game loop effect
  useEffect(() => {
    if (status !== 'playing') return;

    const interval = setInterval(tick, speed);

    return () => clearInterval(interval);
  }, [status, speed, tick]);

  // Start game
  const startGame = useCallback(() => {
    const initialSnake = getInitialSnakePosition();
    setSnake(initialSnake);
    setDirection(DIRECTIONS.RIGHT);
    setScore(0);
    setSpeed(INITIAL_SPEED);
    setStatus('playing');
    spawnFood(initialSnake);
  }, [spawnFood]);

  // Pause game
  const pauseGame = useCallback(() => {
    if (status === 'playing') {
      setStatus('paused');
    }
  }, [status]);

  // Resume game
  const resumeGame = useCallback(() => {
    if (status === 'paused') {
      setStatus('playing');
    }
  }, [status]);

  // Restart game
  const restartGame = useCallback(() => {
    startGame();
  }, [startGame]);

  // Toggle sound
  const toggleSound = useCallback(() => {
    const newValue = !soundEnabled;
    setSoundEnabledState(newValue);
    setSoundEnabled(newValue);
  }, [soundEnabled]);

  return {
    snake,
    food,
    status,
    score,
    speed,
    direction,
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
  };
};
