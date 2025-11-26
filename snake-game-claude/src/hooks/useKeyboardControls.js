import { useEffect } from 'react';
import { DIRECTIONS } from '../utils/gameConfig';

export const useKeyboardControls = (changeDirection, status) => {
  useEffect(() => {
    const handleKeyPress = (event) => {
      // Only respond to keys when game is playing
      if (status !== 'playing') return;

      switch (event.key) {
        case 'ArrowUp':
        case 'w':
        case 'W':
          event.preventDefault();
          changeDirection(DIRECTIONS.UP);
          break;
        case 'ArrowDown':
        case 's':
        case 'S':
          event.preventDefault();
          changeDirection(DIRECTIONS.DOWN);
          break;
        case 'ArrowLeft':
        case 'a':
        case 'A':
          event.preventDefault();
          changeDirection(DIRECTIONS.LEFT);
          break;
        case 'ArrowRight':
        case 'd':
        case 'D':
          event.preventDefault();
          changeDirection(DIRECTIONS.RIGHT);
          break;
        default:
          break;
      }
    };

    window.addEventListener('keydown', handleKeyPress);

    return () => {
      window.removeEventListener('keydown', handleKeyPress);
    };
  }, [changeDirection, status]);
};
