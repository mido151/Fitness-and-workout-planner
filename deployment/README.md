# Deployment – Phase 2 (static prototype)

The Phase 2 prototype is plain HTML + one compiled CSS file, so it can be hosted on any
static web host. Nothing runs on a server.

## 1. Build the CSS
```bash
cd frontend
npm install
npm run build          # writes frontend/css/output.css (minified)
```
`node_modules/` is ignored by git and is not needed on the host.

## 2. What to upload
Everything inside `frontend/` except `node_modules/`:
```
frontend/*.html
frontend/css/output.css
frontend/images/
```

## 3. Hosting options
- **Local preview:** `npx serve frontend` (or VS Code Live Server), then open the printed URL.
- **GitHub Pages:** repository Settings → Pages → deploy from branch `main`, folder `/` and
  open `/frontend/index.html`, or publish the `frontend/` folder with a Pages workflow.
- **Netlify / Vercel:** drag and drop the built `frontend/` folder, or set
  build command `npm run build` and publish directory `frontend` with base directory `frontend`.

## 4. Environment
- Node.js 20+ is only needed to build the CSS.
- External resources loaded at runtime: Google Fonts (Inter, Outfit) and Material Symbols.
  Without internet the pages still work; icons fall back to their text names.
- No environment variables or database in Phase 2. Mock API setup is added in Phase 4.

## 5. Course submission
The version uploaded to Moodle / Google Classroom is the one graded. Before zipping:
1. Merge all team branches into `main` and pull.
2. Run `npm run build` in `frontend/` and check that `css/output.css` is up to date.
3. Zip the repository **without** `node_modules/`.
