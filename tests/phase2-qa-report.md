# Phase 2 – Final QA report (all pages)

QA owner: Mohamed · Date: 28 Oct 2026 · Branch checked: `mido` (main + Mohamed's fixes)

## How it was tested
- **Build:** fresh clone → `cd frontend && npm install && npm run build` (Tailwind v4.3.3 CLI). Builds with no errors and reproduces the committed `css/output.css`.
- **Automated a11y:** [axe-core](https://github.com/dequelabs/axe-core) 4.14, rule sets WCAG 2.0/2.1 A + AA and best-practice, run on every page at 375 px and 1280 px.
- **Responsive:** each page rendered in Chromium at **375 px** (phone), **768 px** (tablet), **1280 px** (desktop); checked for horizontal page scroll and reviewed the full-page screenshots in [`screenshots/`](./screenshots).
- **Keyboard:** Tab order, visible focus ring, skip link, radio groups with arrow keys (login, register, food log).
- **Script:** [`qa/qa.py`](./qa/qa.py) — rerun with `cd tests/qa && npm install && python3 qa.py ../../frontend ./out`.

## Results per page

| Page | Owner | Tailwind build (no CDN) | Inline `<style>` | Overflow 375 / 768 / 1280 | axe violations | Status |
|---|---|---|---|---|---|---|
| index.html | Mohamed | ✅ | removed | ✅ / ✅ / ✅ | 0 | Done |
| login.html | Mohamed | ✅ | removed | ✅ / ✅ / ✅ | 0 | Done |
| register.html | Mohamed | ✅ | removed | ✅ / ✅ / ✅ | 0 | Done |
| food-log.html | Mohamed | ✅ | removed | ✅ / ✅ / ✅ | 0 | Done |
| dashboard.html | Rahma | ✅ | still there | ✅ / ✅ / ✅ | 1 (moderate) | Small fixes |
| exercises.html | Rahma | ✅ | still there | ✅ / ✅ / ✅ | 1 (moderate) | Small fixes |
| exercise-detail.html | Rahma | ✅ | still there | ✅ / ✅ / ✅ | 2 (moderate) | Small fixes |
| routine-builder.html | Lama | ❌ CDN | still there | ✅ / ✅ / ✅ \* | 4 (1 critical, 1 serious) | **Needs work** |
| profile.html | Lama | ❌ CDN | still there | ✅ / ✅ / ✅ \* | 2 (1 serious) | **Needs work** |
| nutrition.html | Lama | ❌ CDN | still there | ✅ / ✅ / ✅ \* | 2 (1 serious) | **Needs work** |

\* The CDN cannot load in the offline test browser, so these three pages were tested with the built `css/output.css` injected instead — i.e. how they will look once switched to the build.

Rubric reminder: "Proper Tailwind build setup (NO CDN)" is 10 points and the project doc says *"You must install Tailwind to your project and don't use the CDN version."*

## What changed in the shared theme (`frontend/src/input.css`)
Everyone should `git pull origin main` after the `mido` PR is merged, then run `npm run build`.
- Font tokens: `font-sans` = Inter, `font-headline` = Outfit (same fonts the pages already load).
- Colour tokens for the dark pages (`night`, `night-card`, `ice`, `mist`, …) and `brand` = sky-700.
- Shared base rules that every page had in its own `<style>`: margin reset, `overscroll-behavior`, hidden scrollbar, **one focus ring for all pages** (sky-700, light blue on dark pages), and reduced-motion support.
- Utilities `frosted-glass`, `glass-card`, `glass-card-subtle` (same CSS as your inline versions).
  → **You can now delete the `<style>` block on your pages** (keep only rules that are truly page-specific, e.g. the number-input spinner rule on routine-builder). Nothing will change visually.

## Issues found on teammates' pages (owners fix their own pages)

### Rahma
1. **dashboard.html – heading order** (axe `heading-order`): the page jumps from `<h1>` (Omar Hassan) to `<h3>` (Upper Body Power…). Change the section titles (lines ~260, 328, 408) from `h3` to `h2` and the exercise names from `h4` to `h3`; keep the same classes.
2. **exercises.html, exercise-detail.html – mobile nav outside landmarks** (axe `region`): the mobile sub-bar is a `<div class="xl:hidden …">`. Change it to `<nav aria-label="Primary (mobile)" …>`.
3. **exercise-detail.html – two unnamed `<nav>`s** (axe `landmark-unique`): add `aria-label="Primary"` to the desktop nav.
4. **All three pages – icons read aloud:** Material Symbols are text ligatures, so a screen reader says "fitness_center", "arrow_forward". Add `aria-hidden="true"` to every `<span class="material-symbols-outlined">`. Icon-only buttons then need a name: `<span class="sr-only">Search</span>` inside the button.
5. Delete the inline `<style>` blocks (now covered by `input.css`).
6. Optional: add a skip link as the first element in `<body>` (copy it from index.html).

### Lama
1. **routine-builder.html, profile.html, nutrition.html – still on the Tailwind CDN.** Replace
   `<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>` with
   `<link rel="stylesheet" href="css/output.css">`, run `npm run build`, and check the page still looks the same (forms plugin is already installed; container queries are built into v4).
2. **Colour contrast (axe `color-contrast`, serious)** on all three pages: white text on `bg-sky-500` (2.7:1) and `bg-sky-600` (4.0:1) fails WCAG AA (needs 4.5:1). Use `bg-sky-700` + `hover:bg-sky-800` for active nav pills and primary buttons, and `text-sky-700` instead of `text-sky-600` for small blue text — the same change Rahma and I made.
3. **routine-builder.html – `#weight-input` has no label** (axe `label`, critical). Add `<label for="weight-input" class="sr-only">Load in kg</label>` or `aria-label="Load in kilograms"`.
4. **All three pages – `<script>` blocks.** Phase 2 asks for a *static prototype (HTML + Tailwind, no interactivity)*. Interactions move to React in Phase 3. Consider removing the scripts and showing one fixed state in HTML (see food-log.html for an example).
5. Same as Rahma 2 and 4: mobile sub-bar → `<nav aria-label="Primary (mobile)">`, `aria-hidden="true"` on icons, unique `aria-label` on the desktop nav.
6. Delete the inline `<style>` blocks (`glass-card`, `glass-card-subtle` now come from `input.css`).

### Whole team
- **Wireframes:** `docs/wireframes/desktop` and `docs/wireframes/mobile` only contain `.gitkeep` and the Figma link. Export desktop (Rahma) and mobile (Lama) frames as PNG/PDF into these folders before submitting — wireframes/mockups are a graded deliverable.
- `npm install` on another OS may rewrite `package-lock.json` (platform-specific optional packages). Don't commit those lock-file changes unless a dependency was really added.

## Checklist status (Work Plan → "Page Checklist" sheet)

| Item | index | login | register | food-log |
|---|---|---|---|---|
| CDN script removed | ✅ | ✅ | ✅ | ✅ |
| Linked css/output.css | ✅ | ✅ | ✅ | ✅ |
| Inline config moved to input.css | ✅ | ✅ | ✅ | ✅ |
| Checked at 375 / 768 / 1280 px | ✅ | ✅ | ✅ | ✅ |
| alt text on images | ✅ no `<img>`; icons `aria-hidden` | ✅ | ✅ | ✅ |
| Labels on all inputs | ✅ n/a | ✅ | ✅ | ✅ |
| aria-label / sr-only name on icon buttons | ✅ | ✅ | ✅ | ✅ |
| Focus states + contrast | ✅ | ✅ | ✅ | ✅ |
| Committed with clear message | ✅ | ✅ | ✅ | ✅ |
