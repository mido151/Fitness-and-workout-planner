# Fit 99 – Fitness & Workout Planner

SW 302 User Interface Development · Course Project · Fall 2026

## Team Members
- Mohamed Sherif Farouk 202401051
- Rahma Ali 202400365
- Lama Omar Zourob 202001711

## Description
A web app to track workout routines, log exercises, and analyze activity over time.

Phase 2 delivers the UI/UX design (wireframes in Figma) and a static prototype of 10 pages
built with HTML5 + Tailwind CSS v4 (installed through npm, no CDN). Every page has a desktop
and a mobile layout.

## Setup

### Requirements
- [Node.js](https://nodejs.org) 20 or newer (includes npm)
- Any modern browser

### Frontend (HTML + Tailwind)
```bash
git clone https://github.com/mido151/Fitness-and-workout-planner.git
cd Fitness-and-workout-planner/frontend
npm install        # installs tailwindcss, @tailwindcss/cli, @tailwindcss/forms
npm run build      # compiles src/input.css -> css/output.css (minified)
```
Then open `frontend/index.html` in a browser (double-click it, or use the VS Code
"Live Server" extension).

While editing pages, run the watcher so the CSS rebuilds on every save:
```bash
npm run dev
```

How the styling works:
- `frontend/src/input.css` is the only Tailwind source file. It holds the shared theme
  (colour and font tokens), base styles and the focus ring used by every page.
- `frontend/css/output.css` is generated. Every page links it with
  `<link rel="stylesheet" href="css/output.css">`. Do not edit it by hand.
- After pulling new commits, run `npm run build` again so `output.css` matches the pages.

### Mock data (backend)
Phase 2 is a static prototype, so there is no data layer yet and `/backend` is empty.
Mock data (JSON Server or the Wger / ExerciseDB API) is added in Phase 4; its run
instructions will be added here then.

## Pages (Phase 2)

| Page | Role in project doc | Owner |
|---|---|---|
| [index.html](frontend/index.html) | Landing / Home | Mohamed |
| [login.html](frontend/login.html) | Authentication – Login | Mohamed |
| [register.html](frontend/register.html) | Authentication – Register | Mohamed |
| [food-log.html](frontend/food-log.html) | Extra page | Mohamed |
| [dashboard.html](frontend/dashboard.html) | Dashboard (cards + charts) | Rahma |
| [exercises.html](frontend/exercises.html) | List / Overview | Rahma |
| [exercise-detail.html](frontend/exercise-detail.html) | Detail | Rahma |
| [routine-builder.html](frontend/routine-builder.html) | Form (add / edit data) | Lama |
| [profile.html](frontend/profile.html) | Extra page | Lama |
| [nutrition.html](frontend/nutrition.html) | Extra page | Lama |

## Repository structure
```
/docs         submitted documents (UI/UX design, wireframes, reports)
/frontend     HTML pages, src/input.css (Tailwind source), css/output.css (built)
/backend      mock data and API integration code (Phase 4)
/tests        test cases and manual test reports
/deployment   deployment and environment setup instructions
```

## Docs
- [Phase 2 docs folder](./docs)
- [Figma wireframes / prototype link](./docs/wireframes/desktop/figma.txt)
- [Desktop wireframes](./docs/wireframes/desktop) · [Mobile wireframes](./docs/wireframes/mobile)
- [Phase 2 QA report](./tests/phase2-qa-report.md)
- [Deployment instructions](./deployment/README.md)
