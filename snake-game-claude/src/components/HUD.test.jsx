import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { HUD } from './HUD';
import { GAME_MODES } from '../utils/gameConfig';

describe('HUD', () => {
  const mockHandlers = {
    onStart: vi.fn(),
    onPause: vi.fn(),
    onResume: vi.fn(),
    onRestart: vi.fn(),
    onModeChange: vi.fn(),
  };

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render without crashing', () => {
    render(<HUD score={0} status="idle" gameMode={GAME_MODES.WALLS} {...mockHandlers} />);
    expect(screen.getByText('Snake Game')).toBeInTheDocument();
  });

  it('should display the correct score', () => {
    render(<HUD score={42} status="playing" gameMode={GAME_MODES.WALLS} {...mockHandlers} />);
    expect(screen.getByText('42')).toBeInTheDocument();
  });

  it('should display score of 0 initially', () => {
    render(<HUD score={0} status="idle" gameMode={GAME_MODES.WALLS} {...mockHandlers} />);
    expect(screen.getByText('0')).toBeInTheDocument();
  });

  describe('idle status', () => {
    it('should show "Press Start to Play" message', () => {
      render(<HUD score={0} status="idle" gameMode={GAME_MODES.WALLS} {...mockHandlers} />);
      expect(screen.getByText('Press Start to Play')).toBeInTheDocument();
    });

    it('should show Start Game button', () => {
      render(<HUD score={0} status="idle" gameMode={GAME_MODES.WALLS} {...mockHandlers} />);
      expect(screen.getByRole('button', { name: /start game/i })).toBeInTheDocument();
    });

    it('should call onStart when Start Game button is clicked', async () => {
      const user = userEvent.setup();
      render(<HUD score={0} status="idle" gameMode={GAME_MODES.WALLS} {...mockHandlers} />);

      const startButton = screen.getByRole('button', { name: /start game/i });
      await user.click(startButton);

      expect(mockHandlers.onStart).toHaveBeenCalledTimes(1);
    });
  });

  describe('playing status', () => {
    it('should show "Playing..." message', () => {
      render(<HUD score={0} status="playing" {...mockHandlers} />);
      expect(screen.getByText('Playing...')).toBeInTheDocument();
    });

    it('should show Pause button', () => {
      render(<HUD score={5} status="playing" gameMode={GAME_MODES.WALLS} {...mockHandlers} />);
      expect(screen.getByRole('button', { name: /pause/i })).toBeInTheDocument();
    });

    it('should call onPause when Pause button is clicked', async () => {
      const user = userEvent.setup();
      render(<HUD score={5} status="playing" gameMode={GAME_MODES.WALLS} {...mockHandlers} />);

      const pauseButton = screen.getByRole('button', { name: /pause/i });
      await user.click(pauseButton);

      expect(mockHandlers.onPause).toHaveBeenCalledTimes(1);
    });
  });

  describe('paused status', () => {
    it('should show "Paused" message', () => {
      render(<HUD score={10} status="paused" gameMode={GAME_MODES.WALLS} {...mockHandlers} />);
      expect(screen.getByText('Paused')).toBeInTheDocument();
    });

    it('should show Resume button', () => {
      render(<HUD score={10} status="paused" gameMode={GAME_MODES.WALLS} {...mockHandlers} />);
      expect(screen.getByRole('button', { name: /resume/i })).toBeInTheDocument();
    });

    it('should show Restart button', () => {
      render(<HUD score={10} status="paused" gameMode={GAME_MODES.WALLS} {...mockHandlers} />);
      expect(screen.getByRole('button', { name: /restart/i })).toBeInTheDocument();
    });

    it('should call onResume when Resume button is clicked', async () => {
      const user = userEvent.setup();
      render(<HUD score={10} status="paused" gameMode={GAME_MODES.WALLS} {...mockHandlers} />);

      const resumeButton = screen.getByRole('button', { name: /resume/i });
      await user.click(resumeButton);

      expect(mockHandlers.onResume).toHaveBeenCalledTimes(1);
    });

    it('should call onRestart when Restart button is clicked', async () => {
      const user = userEvent.setup();
      render(<HUD score={10} status="paused" gameMode={GAME_MODES.WALLS} {...mockHandlers} />);

      const restartButton = screen.getByRole('button', { name: /restart/i });
      await user.click(restartButton);

      expect(mockHandlers.onRestart).toHaveBeenCalledTimes(1);
    });
  });

  describe('gameover status', () => {
    it('should show "Game Over!" message', () => {
      render(<HUD score={25} status="gameover" gameMode={GAME_MODES.WALLS} {...mockHandlers} />);
      expect(screen.getByText('Game Over!')).toBeInTheDocument();
    });

    it('should show Play Again button', () => {
      render(<HUD score={25} status="gameover" gameMode={GAME_MODES.WALLS} {...mockHandlers} />);
      expect(screen.getByRole('button', { name: /play again/i })).toBeInTheDocument();
    });

    it('should call onRestart when Play Again button is clicked', async () => {
      const user = userEvent.setup();
      render(<HUD score={25} status="gameover" gameMode={GAME_MODES.WALLS} {...mockHandlers} />);

      const playAgainButton = screen.getByRole('button', { name: /play again/i });
      await user.click(playAgainButton);

      expect(mockHandlers.onRestart).toHaveBeenCalledTimes(1);
    });

    it('should display final score after game over', () => {
      render(<HUD score={100} status="gameover" gameMode={GAME_MODES.WALLS} {...mockHandlers} />);
      expect(screen.getByText('100')).toBeInTheDocument();
    });
  });

  it('should always show instructions', () => {
    render(<HUD score={0} status="idle" gameMode={GAME_MODES.WALLS} {...mockHandlers} />);
    expect(screen.getByText(/use arrow keys or wasd to move/i)).toBeInTheDocument();
  });

  describe('game mode selector', () => {
    it('should display mode selector with both options', () => {
      render(<HUD score={0} status="idle" gameMode={GAME_MODES.WALLS} {...mockHandlers} />);
      expect(screen.getByText('Mode:')).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /walls/i })).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /pass-through/i })).toBeInTheDocument();
    });

    it('should highlight walls mode when active', () => {
      render(<HUD score={0} status="idle" gameMode={GAME_MODES.WALLS} {...mockHandlers} />);
      const wallsButton = screen.getByRole('button', { name: /walls/i });
      expect(wallsButton).toHaveClass('active');
    });

    it('should highlight pass-through mode when active', () => {
      render(<HUD score={0} status="idle" gameMode={GAME_MODES.PASS_THROUGH} {...mockHandlers} />);
      const passThroughButton = screen.getByRole('button', { name: /pass-through/i });
      expect(passThroughButton).toHaveClass('active');
    });

    it('should call onModeChange with WALLS when walls button is clicked', async () => {
      const user = userEvent.setup();
      render(<HUD score={0} status="idle" gameMode={GAME_MODES.PASS_THROUGH} {...mockHandlers} />);

      const wallsButton = screen.getByRole('button', { name: /^walls$/i });
      await user.click(wallsButton);

      expect(mockHandlers.onModeChange).toHaveBeenCalledWith(GAME_MODES.WALLS);
    });

    it('should call onModeChange with PASS_THROUGH when pass-through button is clicked', async () => {
      const user = userEvent.setup();
      render(<HUD score={0} status="idle" gameMode={GAME_MODES.WALLS} {...mockHandlers} />);

      const passThroughButton = screen.getByRole('button', { name: /pass-through/i });
      await user.click(passThroughButton);

      expect(mockHandlers.onModeChange).toHaveBeenCalledWith(GAME_MODES.PASS_THROUGH);
    });

    it('should disable mode buttons when game is playing', () => {
      render(<HUD score={10} status="playing" gameMode={GAME_MODES.WALLS} {...mockHandlers} />);

      const wallsButton = screen.getByRole('button', { name: /walls/i });
      const passThroughButton = screen.getByRole('button', { name: /pass-through/i });

      expect(wallsButton).toBeDisabled();
      expect(passThroughButton).toBeDisabled();
    });

    it('should enable mode buttons when game is not playing', () => {
      render(<HUD score={0} status="idle" gameMode={GAME_MODES.WALLS} {...mockHandlers} />);

      const wallsButton = screen.getByRole('button', { name: /walls/i });
      const passThroughButton = screen.getByRole('button', { name: /pass-through/i });

      expect(wallsButton).not.toBeDisabled();
      expect(passThroughButton).not.toBeDisabled();
    });
  });
});
