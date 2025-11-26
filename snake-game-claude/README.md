# Snake Game

A classic Snake game built with React and Vite, featuring smooth gameplay, responsive design, and modern UI.

## Features

- **Classic Snake Gameplay**: Navigate the snake to eat food and grow longer
- **Two Game Modes**:
  - **Walls Mode**: Traditional gameplay where hitting walls ends the game
  - **Pass-Through Mode**: Snake wraps around to the opposite side when reaching edges
- **High Score Tracking**: Best score persists using localStorage
- **Sound Effects**:
  - Eating food sound
  - Game over sound
  - New high score celebration
  - Toggle sound on/off with one click
- **Smooth Animations**:
  - Pulsing snake head
  - Glowing food
  - Fade-in effects for snake body
- **Responsive Controls**:
  - Keyboard: Arrow keys or WASD
  - Mobile: Touch-friendly on-screen controls
- **Progressive Difficulty**: Game speeds up as you eat more food
- **Score Tracking**: Real-time score display with persistent high score
- **Pause & Resume**: Take a break without losing your game
- **Clean UI**: Modern dark theme with polished animations

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn

### Installation

1. Navigate to the project directory:
```bash
cd snake-game-claude
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

4. Open your browser and navigate to `http://localhost:5173`

## How to Play

1. Choose your preferred **Game Mode**:
   - **Walls**: Traditional mode where hitting walls ends the game
   - **Pass-Through**: Snake wraps around edges to the opposite side
2. Click **Start Game** to begin
3. Use **Arrow Keys** or **WASD** to control the snake's direction
4. Eat the red food to grow and increase your score
5. Avoid hitting yourself
6. Try to achieve the highest score possible!

**Note**: Game mode can only be changed when the game is not active (idle, paused, or game over).

## Game Controls

| Action | Keyboard | Mobile |
|--------|----------|--------|
| Move Up | ↑ or W | ▲ Button |
| Move Down | ↓ or S | ▼ Button |
| Move Left | ← or A | ◄ Button |
| Move Right | → or D | ► Button |

## Architecture

The game follows a clean, modular architecture:

- **Hooks**: `useSnakeGame` for game logic, `useKeyboardControls` for input
- **Components**: `GameBoard`, `HUD`, `Controls`
- **Utils**: Board configuration and coordinate helpers
- **Game Loop**: Interval-based ticking system with collision detection

## Testing

The project includes comprehensive unit tests using Vitest and React Testing Library.

### Running Tests

```bash
# Run tests in watch mode
npm test

# Run tests once
npm test -- --run

# Run tests with UI
npm run test:ui

# Run tests with coverage
npm run test:coverage
```

### Test Coverage

The test suite includes **66 tests** covering:
- **Utility Functions**: Coordinate helpers, collision detection, boundary checks, pass-through wrapping
- **Game Logic Hook**: Snake movement, direction changes, collision detection, score tracking, game modes
- **Components**: GameBoard rendering, HUD state management, user interactions, and mode toggling

All components and critical game logic are thoroughly tested to ensure reliability.

## Building for Production

To create a production build:

```bash
npm run build
```

The optimized files will be in the `dist` directory.

## Deployment

The game can be deployed to multiple platforms. See [DEPLOYMENT.md](./DEPLOYMENT.md) for comprehensive deployment guides including:

- **Vercel**: Zero-configuration deployment with automatic deployments
- **GitHub Pages**: Free hosting directly from your repository
- **AWS S3/CloudFront**: Scalable hosting with CDN distribution

Each platform includes:
- ✅ Step-by-step manual deployment instructions
- ✅ GitHub Actions workflow for automated CI/CD
- ✅ Configuration examples and best practices

Quick deploy:
```bash
# Vercel (easiest)
npm install -g vercel
vercel

# GitHub Pages
npm install -D gh-pages
npx gh-pages -d dist

# AWS S3
aws s3 sync dist/ s3://your-bucket-name --delete
```

## Development

### Project Structure

```
src/
├── components/       # React components
│   ├── GameBoard.jsx
│   ├── HUD.jsx
│   └── Controls.jsx
├── hooks/           # Custom React hooks
│   ├── useSnakeGame.js
│   └── useKeyboardControls.js
├── utils/           # Utility functions
│   ├── gameConfig.js
│   └── coordinateHelpers.js
├── App.jsx          # Main app component
└── main.jsx         # App entry point
```

### Technologies Used

- **React**: UI library
- **Vite**: Build tool and dev server
- **Vitest**: Testing framework
- **React Testing Library**: Component testing utilities
- **CSS3**: Styling with modern features

## License

MIT
