# Snake Game (React + Vite + TypeScript)

Small React/Vite project for a classic Snake game, built incrementally.

## Scaffold Workflow
- From the repo root, create the app with the Vite React TS template:
  ```bash
  npm create vite@latest snake-game -- --template react-ts
  ```
- Install dependencies:
  ```bash
  cd snake-game
  npm install
  ```
- Create folders for upcoming work:
  ```bash
  mkdir -p src/components src/hooks src/utils
  ```

## Run Locally
- Development server (HMR):
  ```bash
  npm run dev
  ```
  Then open the printed localhost URL (defaults to http://localhost:5173).

- Type-check and build for production:
  ```bash
  npm run build
  ```

- Preview the production build locally:
  ```bash
  npm run preview
  ```

## Build & Deploy
- Create a production build (outputs to `dist/`):
  ```bash
  npm run build
  ```
- Serve the built assets locally to verify:
  ```bash
  npm run preview
  ```
- Deploy the `dist/` folder to any static host (e.g., Netlify, Vercel, GitHub Pages, S3/CloudFront, nginx). No server code is required.

### Vercel
1) Install the Vercel CLI if desired: `npm i -g vercel`.
2) From `snake-game/`, run `npm run build` then `vercel deploy --prebuilt` (or use the dashboard and select this directory).
3) Ensure the project root is `snake-game/` and build command is `npm run build` with output `dist`.

### GitHub Pages
1) Build the app: `npm run build`.
2) Use the provided workflow (`.github/workflows/deploy.yml`):
   - Builds with `npm run build -- --base=/${{ github.event.repository.name }}/` by default.
   - Uploads `dist/` as a Pages artifact and deploys with `actions/deploy-pages`.
3) If your site is served from a custom domain or root (e.g., `user.github.io`), set `BASE_PATH=/` in the workflow or adjust `base` in `vite.config.ts`.

### S3 + CloudFront
1) Build: `npm run build`.
2) Sync `dist/` to your bucket:
   ```bash
   aws s3 sync dist/ s3://your-bucket-name --delete
   ```
3) For CloudFront, create/invalidate a distribution pointing to the bucket (origin access recommended). Invalidate after deploy:
   ```bash
   aws cloudfront create-invalidation --distribution-id YOUR_DIST_ID --paths "/*"
   ```

## Tests
- Run unit and hook tests (Vitest + Testing Library):
  ```bash
  npm test
  ```
  Vitest uses a jsdom environment. If you add new tests, remember to import `vi` timers for loop-based logic.
