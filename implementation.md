## Snake Game Plan (React + Vite)

### Architecture
- App shell renders HUD + GameBoard; optional Controls for on-screen buttons.
- Game state: `snake` (array of cells), `direction`, `food`, `status` (`idle` | `playing` | `paused` | `gameover`), `speed`, `score`.
- Game loop: timer tick moves snake, resolves food, checks collisions (walls/self), updates status.
- Input: keyboard arrows/WASD; optional touch/click controls; block 180° reversal.
- Utilities: board config (rows/cols), coordinate helpers (cell → index, random empty cell), reset/spawn logic.

### Step-by-step Development
1) Bootstrap Vite + React app; add `components/`, `hooks/`, `utils/`, and styles scaffold.
2) Define board config (e.g., 20x20 grid, cell size) and coordinate helpers (grid bounds, random free cell).
3) Build `useSnakeGame` hook:
   - State for snake, direction, food, status, score, speed.
   - Start/pause/resume/restart handlers.
   - Game loop with interval ticking; prevent reverse direction; grow snake on food; increase score; optional speed-up.
   - Collision detection for walls and self; end game on hit.
4) Implement `GameBoard` component to render the grid; highlight snake head/body and food.
5) Add input handling: keyboard listeners; optional on-screen arrow buttons for mobile.
6) Create HUD: score display, status text, start/pause/restart buttons.
7) Style pass: simple responsive layout; clear colors for snake/food/background.
8) Test flows: start → move → eat → grow; self/wall collisions; pause/resume; restart; rapid turns.
9) Optional polish: high score via localStorage, sound toggle, small animations for food/snake.
